# Crawler Architecture Documentation

## 1. High-Level Overview

The Crawler is a Python package designed to crawl web pages and convert their content into Markdown format. The architecture follows object-oriented design principles with a focus on extensibility, separation of concerns, and reusability.

The system is built around a graph-based crawling approach where:
- Nodes represent web pages or other crawlable entities
- Edges represent connections between these entities (e.g., hyperlinks between web pages)
- The crawling process uses a Breadth-First Search (BFS) algorithm to traverse the graph

The architecture is designed to be extensible, allowing for different types of crawlers (web, file system, etc.) to be implemented by extending the base classes.

## 2. Core Components

### 2.1 Base Components

#### 2.1.1 BaseCrawler

`BaseCrawler` is an abstract base class that defines the interface for crawling operations. It implements the core BFS algorithm for traversing a graph structure but delegates specific operations to subclasses through abstract methods.

Key responsibilities:
- Defining the crawling algorithm using BFS
- Managing the crawling process
- Tracking visited nodes
- Building a subgraph of the crawled structure

#### 2.1.2 BaseNode

`BaseNode` is an abstract base class that represents a node in the graph. It provides:
- A unique identifier for each node
- Properties for tracking depth in the graph
- Parent-child relationships for navigation
- An abstract method for converting content to Markdown

#### 2.1.3 BaseGraph

`BaseGraph` encapsulates a directed graph using NetworkX and provides methods for:
- Adding nodes and edges
- Retrieving nodes
- Visualizing the graph
- Converting nodes to Markdown
- Saving content to files (single or multiple)

### 2.2 Web-Specific Components

#### 2.2.1 WebCrawler

`WebCrawler` extends `BaseCrawler` to implement web-specific crawling functionality:
- Retrieving web pages
- Handling domain restrictions
- Managing crawling sessions
- Extracting hyperlinks from web pages

#### 2.2.2 WebNode

`WebNode` extends `BaseNode` to represent a web page:
- Lazily fetching and parsing HTML content
- Extracting hyperlinks
- Converting HTML to Markdown
- Caching content to avoid redundant network requests

#### 2.2.3 WebGraph

`WebGraph` extends `BaseGraph` to provide web-specific graph functionality:
- Custom string and HTML representations
- Visualization enhancements for web graphs

### 2.3 Utility Components

#### 2.3.1 File Utilities

The `file_utils` module provides functions for:
- Generating safe filenames from URLs
- Saving content to multiple files
- Combining content into a single file

## 3. Design Patterns and Component Relationships

### 3.1 Design Patterns

The Crawler architecture employs several design patterns to achieve its goals:

1. **Template Method Pattern**: The `BaseCrawler` class defines the skeleton of the crawling algorithm in its `crawl` method, while deferring specific steps to subclasses through abstract methods like `get_node`, `start_new_crawling_session`, and `visit_node_neighborhood`.

2. **Strategy Pattern**: The crawling behavior can be varied by implementing different crawler strategies (e.g., `WebCrawler`) that conform to the `BaseCrawler` interface.

3. **Factory Method Pattern**: The `get_node` method in `BaseCrawler` acts as a factory method, creating nodes of the appropriate type for the specific crawler implementation.

4. **Composite Pattern**: The graph structure represents a composite pattern where both individual nodes and the entire graph can be treated uniformly through common interfaces.

5. **Lazy Loading**: The `WebNode` class uses lazy loading to fetch and parse HTML content only when needed, improving performance by avoiding unnecessary network requests.

6. **Adapter Pattern**: The `html2text` library is used as an adapter to convert HTML content to Markdown format.

### 3.2 Component Relationships

The architecture follows a clear hierarchy:

1. **Base Layer**: Abstract classes (`BaseCrawler`, `BaseNode`, `BaseGraph`) define the core interfaces and functionality.

2. **Implementation Layer**: Concrete classes (`WebCrawler`, `WebNode`, `WebGraph`) implement the interfaces for specific domains (web crawling).

3. **Utility Layer**: Helper functions and modules provide supporting functionality.

The relationships between components are as follows:

- `BaseCrawler` uses `BaseNode` objects to represent entities and builds a `BaseGraph` during crawling.
- `WebCrawler` extends `BaseCrawler` and works with `WebNode` objects to represent web pages.
- `WebCrawler` builds a `WebGraph` during the crawling process.
- `WebNode` fetches and parses HTML content, extracts hyperlinks, and converts content to Markdown.
- `WebGraph` provides visualization and export functionality for the crawled web structure.
- Utility functions in `file_utils` are used by `BaseGraph` (and by extension, `WebGraph`) to save content to files.

## 4. Control Flow

### 4.1 Crawling Process

1. **Initialization**:
   - A `WebCrawler` instance is created with optional domain restrictions.
   - A starting URL is provided to the `crawl` method.

2. **Crawling**:
   - The crawler creates a `WebNode` for the starting URL.
   - It initializes a new `WebGraph` for the crawling session.
   - Using BFS, it explores the web graph up to the specified depth:
     - For each node, it fetches the web page and extracts hyperlinks.
     - It creates new `WebNode` instances for each hyperlink within allowed domains.
     - It adds these nodes and their connections to the `WebGraph`.

3. **Output**:
   - The resulting `WebGraph` contains all visited nodes and their connections.
   - This graph can be visualized or exported to Markdown files.

### 4.2 Command-Line Interface

The package provides a command-line interface through the `main` function in `__init__.py`:

1. **Argument Parsing**:
   - The user provides command-line arguments including the starting URL, output folder, and options.

2. **Crawling**:
   - A `WebCrawler` is initialized with the specified allowed domains.
   - The crawler performs the crawl starting from the provided URL.

3. **Output**:
   - The user can choose to visualize the crawled graph.
   - The crawled data can be saved as multiple Markdown files or combined into a single file.

## 5. Usage Examples

### 5.1 Basic Usage

```python
from crawler.web.web_crawler import WebCrawler

# Initialize a web crawler with domain restrictions
crawler = WebCrawler(allowed_domains=["example.com"])

# Perform a crawl starting from a URL with a maximum depth of 2
crawl_graph = crawler.crawl("https://www.example.com", max_depth=2)

# Save the crawled content to multiple Markdown files
crawl_graph.save_to_multiple_files(directory="output")
```

### 5.2 Combining Multiple URLs

```python
from crawler.web.web_crawler import WebCrawler

# Initialize a web crawler
crawler = WebCrawler()

# Crawl multiple URLs and combine the results
urls = ["https://www.example.com", "https://www.another-example.com"]
combined_graph = crawler.crawl_multiple_urls(urls, max_depth=1)

# Save the combined content to a single Markdown file
combined_graph.save_to_single_file(directory="output", filename="combined.md")
```

### 5.3 Visualization

```python
from crawler.web.web_crawler import WebCrawler

# Initialize a web crawler
crawler = WebCrawler()

# Perform a crawl
crawl_graph = crawler.crawl("https://www.example.com", max_depth=1)

# Visualize the crawled graph
crawl_graph.visualize()
```

### 5.4 Command-Line Usage

```bash
# Basic usage
crawler -u https://www.example.com -o output/

# Crawl with a maximum depth of 3
crawler -u https://www.example.com -o output/ -md 3

# Restrict crawling to specific domains
crawler -u https://www.example.com -o output/ -ad example.com sub.example.com

# Combine all pages into a single Markdown file
crawler -u https://www.example.com -o output/ -c

# Visualize the crawled graph
crawler -u https://www.example.com -o output/ -vis
```

## 6. Extension Points

The architecture is designed to be extensible in several ways:

### 6.1 New Crawler Types

New crawler types can be implemented by extending the `BaseCrawler` class and implementing its abstract methods:

```python
class FilesystemCrawler(BaseCrawler):
    def get_node(self, node_id):
        # Implement to return a node representing a file or directory
        pass

    def start_new_crawling_session(self, start_node_id):
        # Implement to initialize a new crawling session
        pass

    def visit_node_neighborhood(self, node):
        # Implement to return neighboring files or directories
        pass
```

### 6.2 New Node Types

New node types can be implemented by extending the `BaseNode` class:

```python
class FileNode(BaseNode):
    def __init__(self, file_path, **attributes):
        super().__init__(file_path, **attributes)
        self._content = None

    def read_content(self):
        # Implement to read file content
        pass

    def to_markdown(self):
        # Implement to convert file content to Markdown
        pass
```

### 6.3 Custom Graph Implementations

Custom graph implementations can be created by extending the `BaseGraph` class:

```python
class FileSystemGraph(BaseGraph):
    def __init__(self):
        super().__init__()

    def visualize(self):
        # Implement custom visualization for file system graphs
        pass
```

### 6.4 Additional Output Formats

The current implementation focuses on Markdown output, but support for additional formats could be added:

```python
def to_html(self):
    # Convert node content to HTML
    pass

def save_to_html_files(self, directory="output"):
    # Save content as HTML files
    pass
```

## 7. Future Enhancements

As outlined in the project's roadmap, several enhancements are planned:

1. **Parallel Crawling**: Implement parallel crawling techniques to improve efficiency.

2. **File System Crawling**: Extend crawling capabilities to local file systems.

3. **GitHub Repository Crawling**: Enable crawling of GitHub repositories to extract code.

4. **Caching with Expiration**: Implement a more sophisticated caching mechanism with expiration times.

5. **Database Support**: Store cached content in a database for more efficient retrieval.

6. **Additional Output Formats**: Support formats beyond Markdown, such as HTML or PDF.

7. **Custom Parsing Rules**: Allow users to define custom parsing rules for specific websites.

8. **Enhanced Visualization**: Improve graph visualization with more interactive features.

## 8. Project Structure and Dependencies

### 8.1 Project Structure

The project is organized into the following directory structure:

```
crawler/
├── crawler/                  # Main package directory
│   ├── __init__.py           # Package initialization and CLI entry point
│   ├── base/                 # Base classes directory
│   │   ├── base_crawler.py   # Abstract base crawler class
│   │   ├── base_graph.py     # Base graph implementation
│   │   └── base_node.py      # Abstract base node class
│   ├── web/                  # Web-specific implementations
│   │   ├── web_crawler.py    # Web crawler implementation
│   │   ├── web_graph.py      # Web graph implementation
│   │   └── web_node.py       # Web node implementation
│   └── utils/                # Utility functions
│       └── file_utils.py     # File handling utilities
├── examples/                 # Example usage
│   └── web_crawler.ipynb     # Jupyter notebook with examples
├── tests/                    # Test directory
├── setup.py                  # Package installation configuration
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

### 8.2 Dependencies

The project relies on the following key dependencies:

- **NetworkX**: For graph data structures and algorithms
- **BeautifulSoup**: For HTML parsing
- **Requests**: For HTTP requests
- **html2text**: For converting HTML to Markdown
- **Matplotlib**: For graph visualization
- **Jupyter/IPyKernel**: For interactive examples

### 8.3 Installation

The package can be installed using pip:

```bash
pip install -e .
```

This installs the package in development mode and creates a console script entry point named `crawler` that maps to the `main` function in the crawler package.

### 8.4 Testing

The project includes a comprehensive test suite using pytest. Tests are organized in the `tests/` directory and cover the main components of the system:

- **test_web_crawler.py**: Tests for the WebCrawler class, including initialization, node retrieval, session management, and domain restrictions.
- **test_web_node.py**: Tests for the WebNode class, including HTML fetching, parsing, hyperlink extraction, and Markdown conversion.
- **test_web_graph.py**: Tests for the WebGraph class, including node and edge management, visualization, and export functionality.
- **test_file_utils.py**: Tests for the file utility functions, including filename generation and file saving operations.

The tests use fixtures to set up reusable objects and mocking to avoid actual network requests, ensuring that tests are fast, reliable, and independent of external resources.

To run the tests:

```bash
pytest
```

For test coverage information:

```bash
coverage run -m pytest
coverage report
```

## 9. Conclusion

The Crawler architecture provides a flexible and extensible framework for crawling web pages and converting their content to Markdown. Its modular design allows for easy extension to support different types of crawling and output formats. The clear separation of concerns between the base classes and their implementations makes the code maintainable and adaptable to future requirements.
