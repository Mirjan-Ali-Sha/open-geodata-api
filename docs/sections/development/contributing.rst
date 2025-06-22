Contributing to Open Geodata API
=================================

We welcome contributions from the community! This guide will help you get started with contributing to Open Geodata API.

Ways to Contribute
------------------

🐛 **Bug Reports**
  Found a bug? Report it on our GitHub Issues page with detailed information.

✨ **Feature Requests**
  Have an idea for a new feature? Create a feature request issue.

📝 **Documentation**
  Help improve our documentation, examples, or tutorials.

💻 **Code Contributions**
  Submit bug fixes, new features, or performance improvements.

🧪 **Testing**
  Help expand our test coverage or improve existing tests.

📚 **Examples**
  Create real-world examples and use cases.

Getting Started
---------------

Development Setup
~~~~~~~~~~~~~~~~~

1. **Fork the repository** on GitHub

2. **Clone your fork**:

.. code-block:: bash

   git clone https://github.com/YOUR_USERNAME/open-geodata-api.git
   cd open-geodata-api

3. **Create a virtual environment**:

.. code-block:: bash

   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

4. **Install development dependencies**:

.. code-block:: bash

   pip install -e .[dev]

5. **Install pre-commit hooks**:

.. code-block:: bash

   pre-commit install

6. **Run tests to verify setup**:

.. code-block:: bash

   pytest

Development Workflow
~~~~~~~~~~~~~~~~~~~~

1. **Create a feature branch**:

.. code-block:: bash

   git checkout -b feature/your-feature-name

2. **Make your changes** following our coding standards

3. **Run tests**:

.. code-block:: bash

   pytest
   pytest --cov=open_geodata_api  # With coverage

4. **Check code style**:

.. code-block:: bash

   black .
   flake8
   mypy open_geodata_api/

5. **Commit your changes**:

.. code-block:: bash

   git add .
   git commit -m "feat: add your feature description"

6. **Push to your fork**:

.. code-block:: bash

   git push origin feature/your-feature-name

7. **Create a Pull Request** on GitHub

Coding Standards
----------------

Code Style
~~~~~~~~~~

We use **Black** for code formatting and **flake8** for linting:

.. code-block:: bash

   # Format code
   black .
   
   # Check style
   flake8
   
   # Type checking
   mypy open_geodata_api/

**Key Style Guidelines:**

- Use **Black** default formatting (88 character line length)
- Follow **PEP 8** naming conventions
- Use **type hints** for all public functions
- Write **descriptive docstrings** for all public APIs
- Keep functions **focused** and **single-purpose**

Documentation Style
~~~~~~~~~~~~~~~~~~~

**Docstring Format** (Google style):

.. code-block:: python

   def search_items(collections, bbox=None, datetime=None):
       """Search for satellite data items.
       
       Args:
           collections: List of collection names to search
           bbox: Bounding box as [west, south, east, north]
           datetime: Date range as string or datetime objects
           
       Returns:
           STACItemCollection: Collection of found items
           
       Raises:
           ValueError: If collection names are invalid
           
       Example:
           >>> pc = ogapi.planetary_computer()
           >>> results = pc.search(['sentinel-2-l2a'], bbox=[-122, 47, -121, 48])
           >>> items = results.get_all_items()
       """

**Comment Guidelines:**

- Use comments sparingly for complex logic
- Prefer **self-documenting code** with clear variable names
- Add **TODO** comments for future improvements
- Use **docstrings** for all public functions and classes

Testing Guidelines
------------------

Test Structure
~~~~~~~~~~~~~~

We use **pytest** for testing:

.. code-block:: text

   tests/
   ├── conftest.py              # Shared fixtures
   ├── test_clients.py          # Client class tests
   ├── test_core.py             # Core STAC class tests
   ├── test_utils.py            # Utility function tests
   ├── test_integration.py      # Integration tests
   └── fixtures/                # Test data
       ├── sample_item.json
       └── sample_collection.json

Writing Tests
~~~~~~~~~~~~~

**Test Naming:**

.. code-block:: python

   def test_search_returns_items():
       """Test that search returns expected items."""
       
   def test_search_with_invalid_collection_raises_error():
       """Test error handling for invalid collections."""

**Test Structure:**

.. code-block:: python

   def test_feature_functionality():
       # Arrange
       client = create_test_client()
       expected_result = "expected_value"
       
       # Act
       result = client.some_method()
       
       # Assert
       assert result == expected_result

**Mocking External APIs:**

.. code-block:: python

   @patch('requests.post')
   def test_search_calls_api_correctly(mock_post):
       mock_post.return_value.json.return_value = sample_response
       
       client = PlanetaryComputerCollections()
       result = client.search(['sentinel-2-l2a'])
       
       mock_post.assert_called_once()

Test Coverage
~~~~~~~~~~~~~

- Aim for **>90% test coverage**
- Test **happy paths** and **error conditions**
- Include **integration tests** for complete workflows
- Mock **external API calls** in unit tests
- Use **real API calls** in integration tests (sparingly)

**Run coverage reports:**

.. code-block:: bash

   pytest --cov=open_geodata_api --cov-report=html
   open htmlcov/index.html  # View coverage report

Pull Request Process
--------------------

Pull Request Guidelines
~~~~~~~~~~~~~~~~~~~~~~~

**Before Submitting:**

- ✅ All tests pass
- ✅ Code follows style guidelines
- ✅ Documentation is updated
- ✅ CHANGELOG.md is updated (for significant changes)
- ✅ Commit messages follow convention

**PR Description Template:**

.. code-block:: text

   ## Description
   Brief description of changes made.
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   
   ## Testing
   - [ ] Added tests for new functionality
   - [ ] All existing tests pass
   - [ ] Manual testing completed
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Documentation updated
   - [ ] Self-review completed

Commit Message Convention
~~~~~~~~~~~~~~~~~~~~~~~~~

We follow **Conventional Commits**:

.. code-block:: text

   <type>(<scope>): <description>
   
   [optional body]
   
   [optional footer]

**Types:**
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

**Examples:**

.. code-block:: text

   feat(core): add support for asset filtering
   
   fix(cli): resolve URL encoding issue in download command
   
   docs(examples): add real-world agricultural monitoring example
   
   test(utils): increase coverage for download functions

Review Process
~~~~~~~~~~~~~~

**What We Look For:**

- ✅ **Functionality**: Does the code work as intended?
- ✅ **Testing**: Are there adequate tests?
- ✅ **Documentation**: Is the change properly documented?
- ✅ **Style**: Does it follow our coding standards?
- ✅ **Performance**: Any performance implications?
- ✅ **Breaking Changes**: Are they necessary and documented?

**Review Timeline:**
- Initial response: Within 1-2 weeks
- Code review: Depends on complexity
- Merge: After approval and CI passes

Release Process
---------------

Versioning
~~~~~~~~~~

We follow **Semantic Versioning** (SemVer):

- **MAJOR** (X.0.0): Breaking changes
- **MINOR** (0.X.0): New features, backwards compatible
- **PATCH** (0.0.X): Bug fixes, backwards compatible

Release Workflow
~~~~~~~~~~~~~~~~

1. **Create release branch**: ``release/vX.Y.Z``
2. **Update version** in ``__init__.py``
3. **Update CHANGELOG.md**
4. **Run full test suite**
5. **Create release PR**
6. **Tag release** after merge
7. **Publish to PyPI** (automated)

Community Guidelines
--------------------

Code of Conduct
~~~~~~~~~~~~~~~

We follow the **Contributor Covenant Code of Conduct**:

- **Be respectful** and inclusive
- **Be collaborative** and helpful
- **Be patient** with newcomers
- **Focus on the project** goals
- **Respect different perspectives**

Communication
~~~~~~~~~~~~~

**Preferred Channels:**
- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: Questions, sharing ideas
- **Pull Requests**: Code review and discussion

**Response Expectations:**
- We aim to respond to issues within a week
- Complex issues may take longer to resolve
- Community contributions help everyone

Getting Recognition
-------------------

Contributors Hall of Fame
~~~~~~~~~~~~~~~~~~~~~~~~~~

All contributors are recognized in:

- **README.md**: Contributors section
- **Documentation**: Acknowledgments page
- **Release Notes**: Major contribution highlights

**Recognition Levels:**
- **Contributor**: Any merged PR
- **Regular Contributor**: Multiple significant PRs
- **Core Contributor**: Ongoing significant contributions
- **Maintainer**: Trusted with repository access

Becoming a Maintainer
~~~~~~~~~~~~~~~~~~~~~

**Path to Maintainer Status:**

1. **Consistent Contributions**: Regular, high-quality PRs
2. **Community Involvement**: Helping others, reviewing PRs
3. **Domain Expertise**: Deep understanding of codebase
4. **Reliability**: Following through on commitments
5. **Leadership**: Guiding project direction

**Maintainer Responsibilities:**
- Review and merge pull requests
- Triage issues and discussions
- Guide project roadmap
- Mentor new contributors
- Maintain code quality standards

Resources for Contributors
--------------------------

**Learning Resources:**
- `Python packaging guide <https://packaging.python.org/>`_
- `Pytest documentation <https://docs.pytest.org/>`_
- `STAC specification <https://stacspec.org/>`_

**Development Tools:**
- `Black code formatter <https://black.readthedocs.io/>`_
- `Flake8 linter <https://flake8.pycqa.org/>`_
- `MyPy type checker <https://mypy.readthedocs.io/>`_
- `Pre-commit hooks <https://pre-commit.com/>`_

**Project Resources:**
- **GitHub Repository**: https://github.com/Mirjan-Ali-Sha/open-geodata-api
- **Documentation**: https://open-geodata-api.readthedocs.io
- **PyPI Package**: https://pypi.org/project/open-geodata-api
- **Examples Repository**: https://github.com/Mirjan-Ali-Sha/open-geodata-api-examples

Thank you for contributing to Open Geodata API! Your contributions help make satellite data more accessible to everyone. 🌍🛰️
