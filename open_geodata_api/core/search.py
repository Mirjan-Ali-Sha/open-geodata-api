"""
STAC Search with silent 3-tier fallback strategy - Enhanced Version
"""

import warnings
from typing import Dict, Optional, Any, List, Union
from .collections import STACItemCollection

try:
    import pystac_client
    import planetary_computer
    PYSTAC_AVAILABLE = True
except ImportError:
    PYSTAC_AVAILABLE = False

class STACSearch:
    """Enhanced STAC Search with silent 3-tier fallback strategy for all methods."""
    
    def __init__(self, search_results: Dict, provider: str = "unknown",
                 client_instance=None, original_search_params: Optional[Dict] = None,
                 search_url: str = None, verbose: bool = False):
        
        self._results = search_results
        self._items = search_results.get('items', search_results.get('features', []))
        self.provider = provider
        self._client = client_instance
        self._original_params = original_search_params or {}
        self._search_url = search_url
        self._verbose = verbose
        
        # Enhanced fallback strategy tracking
        self._fallback_attempted = False
        self._pystac_attempted = False
        self._chunking_attempted = False
        
        # Enhanced caching system
        self._all_items_cached = search_results.get('all_items_cached', False)
        self._all_items_cache = None
        self._fallback_metadata_cache = {}
        
        # If all items are already cached, set them up immediately
        if self._all_items_cached:
            self._all_items_cache = STACItemCollection(self._items, provider=self.provider)
    
    def _ensure_fallback_data(self) -> bool:
        """🔄 Generic fallback data retrieval - used by multiple methods."""
        if self._all_items_cache:
            return True
            
        # Try to get all items using existing fallback strategy
        try:
            self._all_items_cache = self.get_all_items()
            return True
        except Exception as e:
            if self._verbose:
                print(f"⚠️ Fallback data retrieval failed: {e}")
            return False
    
    def get_all_items(self) -> STACItemCollection:
        """🔄 3-TIER FALLBACK: Simple → pystac-client → chunking (silent by default)."""
        # If all items are already cached, return immediately
        if self._all_items_cache:
            return self._all_items_cache
        
        # If items were already fetched during search, use them
        if self._all_items_cached:
            self._all_items_cache = STACItemCollection(self._items, provider=self.provider)
            return self._all_items_cache
        
        # Start fallback strategy if not already attempted
        if not self._fallback_attempted and self._client:
            self._fallback_attempted = True
            
            # 🔄 STEP 1: Check if we need fallback (exactly 100 items = likely truncated)
            if len(self._items) == 100:
                if self._verbose:
                    print(f"🔄 Detected {len(self._items)} items - attempting fallback strategies...")
                
                # 🔄 STEP 2: Try pystac-client first
                pystac_result = self._try_pystac_fallback()
                if pystac_result:
                    return pystac_result
                
                # 🔄 STEP 3: Try chunking search as last resort
                chunking_result = self._try_chunking_fallback()
                if chunking_result:
                    return chunking_result
                
                if self._verbose:
                    print("⚠️ All fallback strategies failed, returning simple search results")
            else:
                if self._verbose:
                    print(f"✅ Simple search returned {len(self._items)} items (no fallback needed)")
        
        # Return simple search results
        return STACItemCollection(self._items, provider=self.provider)
    
    def _try_pystac_fallback(self) -> Optional[STACItemCollection]:
        """🔄 FALLBACK TIER 2: Try pystac-client pagination (silent)."""
        if self._pystac_attempted or not PYSTAC_AVAILABLE:
            return None
            
        self._pystac_attempted = True
        
        try:
            if self._verbose:
                print("🔄 Tier 2: Trying pystac-client fallback...")
            
            # Create pystac-client catalog for this provider
            pystac_catalog = self._client._create_pystac_catalog_fallback()
            if not pystac_catalog:
                if self._verbose:
                    print("  ❌ pystac-client catalog creation failed")
                return None
            
            # Create pystac-client search
            pystac_search = pystac_catalog.search(**self._original_params)
            
            # 🔇 SUPPRESS DEPRECATION WARNING
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=FutureWarning, module="pystac_client")
                warnings.filterwarnings("ignore", message=".*get_all_items.*deprecated.*")
                
                # Get all items using pystac-client's magic (suppressed warnings)
                pystac_items = pystac_search.get_all_items()
                all_items_dicts = [item.to_dict() for item in pystac_items]
            
            if self._verbose:
                print(f"  ✅ pystac-client retrieved {len(all_items_dicts)} total items")
            
            # Cache metadata from pystac search
            self._fallback_metadata_cache['pystac_matched'] = len(all_items_dicts)
            
            # Cache and return
            self._all_items_cache = STACItemCollection(all_items_dicts, provider=self.provider)
            self._all_items_cached = True
            return self._all_items_cache
            
        except Exception as e:
            if self._verbose:
                print(f"  ❌ pystac-client fallback failed: {e}")
            return None
    
    def _try_chunking_fallback(self) -> Optional[STACItemCollection]:
        """🔄 FALLBACK TIER 3: Try own chunking search (silent)."""
        if self._chunking_attempted:
            return None
            
        self._chunking_attempted = True
        
        try:
            if self._verbose:
                print("🔄 Tier 3: Trying chunking fallback...")
            
            # Use client's chunking method if available
            if hasattr(self._client, '_fallback_chunking_search'):
                chunked_items = self._client._fallback_chunking_search(
                    self._original_params,
                    self._search_url,
                    verbose=self._verbose
                )
                
                if self._verbose:
                    print(f"  ✅ Chunking retrieved {len(chunked_items)} total items")
                
                # Cache metadata from chunking search
                self._fallback_metadata_cache['chunking_matched'] = len(chunked_items)
                
                # Cache and return
                self._all_items_cache = STACItemCollection(chunked_items, provider=self.provider)
                self._all_items_cached = True
                return self._all_items_cache
            else:
                if self._verbose:
                    print("  ❌ Chunking method not available")
                return None
                
        except Exception as e:
            if self._verbose:
                print(f"  ❌ Chunking fallback failed: {e}")
            return None
    
    def item_collection(self) -> STACItemCollection:
        """Alias for get_all_items()."""
        return self.get_all_items()
    
    def items(self):
        """🔄 ENHANCED: Return iterator over ALL items with fallback support."""
        # Try to get all items using fallback strategy
        if self._ensure_fallback_data():
            # Use cached complete item collection
            for item_data in self._all_items_cache.items:
                from .items import STACItem
                yield STACItem(item_data, provider=self.provider)
        else:
            # Fallback to original behavior
            for item_data in self._items:
                from .items import STACItem
                yield STACItem(item_data, provider=self.provider)
    
    def matched(self) -> Optional[int]:
        """🔄 ENHANCED: Return total number of matched items with fallback support."""
        # Try fallback sources first
        if 'pystac_matched' in self._fallback_metadata_cache:
            return self._fallback_metadata_cache['pystac_matched']
        
        if 'chunking_matched' in self._fallback_metadata_cache:
            return self._fallback_metadata_cache['chunking_matched']
        
        # Try to get accurate count from fallback data
        if self._ensure_fallback_data():
            count = len(self._all_items_cache.items)
            self._fallback_metadata_cache['fallback_matched'] = count
            return count
        
        # Original behavior
        return self._results.get('numberMatched', self._results.get('matched'))
    
    def total_items(self) -> Optional[int]:
        """🔄 ENHANCED: Return total number of items with fallback support."""
        # Try to get accurate count from fallback data
        if self._ensure_fallback_data():
            count = len(self._all_items_cache.items)
            self._fallback_metadata_cache['fallback_total'] = count
            return count
        
        # Original behavior
        return self._results.get('total_returned')
    
    def search_params(self) -> Optional[dict]:
        """Return search parameters used for the query."""
        return self._results.get('search_params', self._original_params)
    
    def all_keys(self) -> List[str]:
        """Return all keys from the search results."""
        return list(self._results.keys())
    
    def list_product_ids(self) -> List[str]:
        """🔄 ENHANCED: Return complete list of product IDs with fallback support."""
        # Try to get complete list from fallback data
        if self._ensure_fallback_data():
            return list({
                item.get('id') for item in self._all_items_cache.items 
                if isinstance(item, dict) and item.get('id')
            })
        
        # Original behavior
        return list({
            item.get('id') for item in self._items 
            if isinstance(item, dict) and item.get('id')
        })
    
    def get_fallback_status(self) -> Dict[str, Any]:
        """🔄 NEW: Get detailed fallback status information."""
        return {
            'fallback_attempted': self._fallback_attempted,
            'pystac_attempted': self._pystac_attempted,
            'chunking_attempted': self._chunking_attempted,
            'all_items_cached': self._all_items_cached,
            'cache_metadata': self._fallback_metadata_cache,
            'original_items_count': len(self._items),
            'cached_items_count': len(self._all_items_cache.items) if self._all_items_cache else None
        }
    
    def __len__(self):
        """🔄 ENHANCED: Return length with fallback support."""
        # Try to get accurate count from fallback data
        if self._ensure_fallback_data():
            return len(self._all_items_cache.items)
        
        # Original behavior
        return len(self._items)
    
    def __repr__(self):
        """🔄 ENHANCED: Enhanced representation with fallback info."""
        count = len(self)
        status = "with fallback" if self._all_items_cached else "simple"
        return f"STACSearch({count} items found, provider='{self.provider}', {status})"
