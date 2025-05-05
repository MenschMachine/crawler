from .web_node import WebNode
from .web_graph import WebGraph
from ..base.base_crawler import BaseCrawler
from typing import List, Optional, Union, Dict, Any, Tuple


class WebCrawler(BaseCrawler):
    """A web crawler for navigating and extracting information from the web, adhering to specified
    domain restrictions.

    This class extends BaseCrawler to specifically handle web pages by fetching and analyzing their hyperlinks. It supports
    starting new crawling sessions with options to restrict crawling to specific domains.

    Parameters
    ----------
    allowed_domains : list of str, optional
        A list specifying domains that the crawler is allowed to access. If empty, no domain restrictions are applied. Defaults to an empty list.

    Attributes
    ----------
    base_allowed_domains : list of str
        The list of domains that the crawler is initially set to access.
    session_allowed_domains : list of str
        Domains that the crawler is allowed to access during a specific crawling session, which can be dynamically adjusted.

    Methods
    -------
    get_node(node_id)
        Retrieves a WebNode instance corresponding to a given node identifier, typically a URL.
    start_new_crawling_session(start_node_id, restrict_to_domain=True)
        Initializes a new crawling session, optionally restricting it to the domain of the start node.
    in_allowed_domain(url)
        Checks whether a given URL falls within the allowed domains for the current session.
    visit_node_neighborhood(node)
        Analyzes a given node (web page) and returns its neighboring nodes (linked web pages) that fall within the allowed domains.

    Examples
    --------
    >>> crawler = WebCrawler(allowed_domains=['example.com'])
    >>> start_node = crawler.get_node('http://example.com')
    >>> crawl_subgraph = crawler.start_new_crawling_session(start_node.id, restrict_to_domain=True)
    >>> neighbors = crawler.visit_node_neighborhood(start_node)
    >>> len(neighbors)
    5  # Assuming the start_node has 5 allowable linked pages.
    """

    def __init__(self, allowed_domains: List[str] = None) -> None:
        """Initializes the WebCrawler with specified domain restrictions.

        Parameters
        ----------
        allowed_domains : list of str, optional
            Specifies the domains that the crawler is allowed to access. Defaults to an empty list, implying no restrictions.
        """
        super().__init__()
        self.base_allowed_domains: List[str] = allowed_domains if allowed_domains is not None else []
        self.session_allowed_domains: List[str] = []

    def get_node(self, node_id: str) -> WebNode:
        """Retrieves a WebNode instance corresponding to a given node identifier (URL).

        Parameters
        ----------
        node_id : str
            The identifier of the node to retrieve, typically a URL.

        Returns
        -------
        WebNode
            The WebNode instance corresponding to the given identifier.
        """
        return WebNode(node_id)

    def start_new_crawling_session(self, start_node_id: str, restrict_to_domain: bool = True) -> WebGraph:
        """Initializes a new crawling session, with an option to restrict the session to the domain
        of the start node.

        Parameters
        ----------
        start_node_id : str
            The identifier of the node from which to start the crawl.
        restrict_to_domain : bool, optional
            If True, restricts the crawling session to the domain of the start node. Defaults to True.

        Returns
        -------
        WebGraph
            An initialized WebGraph instance for the new crawling session.
        """
        start_node: WebNode = self.get_node(start_node_id)
        if restrict_to_domain:
            self.session_allowed_domains = [start_node.domain]
        else:
            self.session_allowed_domains = []
        crawl_subgraph: WebGraph = WebGraph()
        crawl_subgraph.add_node(start_node)
        return crawl_subgraph

    def in_allowed_domain(self, url: str) -> bool:
        """Determines if the given URL is within the crawler's allowed domains for the current
        session.

        Parameters
        ----------
        url : str
            The URL to check against the allowed domains.

        Returns
        -------
        bool
            True if the URL is within the allowed domains, False otherwise.
        """
        all_allowed_domains: List[str] = self.base_allowed_domains + self.session_allowed_domains
        return len(all_allowed_domains) == 0 or any(
            domain in url for domain in all_allowed_domains
        )

    def visit_node_neighborhood(self, node: WebNode) -> List[WebNode]:
        """Fetches the web page corresponding to the given node, extracts links, and returns
        neighboring nodes within allowed domains.

        Parameters
        ----------
        node : WebNode
            The node whose neighborhood is to be visited.

        Returns
        -------
        list of WebNode
            A list of WebNode instances representing the allowable neighboring nodes linked from the given node.
        """
        node_neighbors: List[str] = node.fetch_connected_hyperlinks()
        allowed_neighbors: List[WebNode] = [
            WebNode(neighbor)
            for neighbor in node_neighbors
            if self.in_allowed_domain(neighbor)
        ]
        return allowed_neighbors

    def crawl_multiple_urls(self, urls: List[str], max_depth: int = 1, max_results: int = None) -> WebGraph:
        """Performs a crawl starting from multiple URLs, building a single graph.

        This method iteratively crawls each URL in the provided list, adding the resulting subgraphs to a
        single `WebGraph` instance.

        Parameters
        ----------
        urls : list of str
            A list of URLs to start crawling from.
        max_depth : int, optional
            The maximum depth to crawl from each starting URL. Defaults to 1.
        max_results : int, optional
            The maximum number of nodes to include in the results. Default is None (no limit).

        Returns
        -------
        WebGraph
            The combined `WebGraph` containing all nodes and edges explored from the provided URLs.
        """
        crawl_subgraph: WebGraph = WebGraph()
        remaining_results = max_results

        for url in urls:
            # If we've reached the maximum number of results, stop crawling
            if max_results is not None and len(crawl_subgraph.all_nodes()) >= max_results:
                break

            # Calculate remaining results for this URL
            if max_results is not None:
                remaining_results = max_results - len(crawl_subgraph.all_nodes())
                if remaining_results <= 0:
                    break

            subgraph: WebGraph = self.crawl(url, max_depth=max_depth, max_results=remaining_results)
            crawl_subgraph.graph.update(subgraph.graph)  # Merge subgraphs

        return crawl_subgraph
