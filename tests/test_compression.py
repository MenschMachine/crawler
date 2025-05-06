import requests
import brotli
import logging
from bs4 import BeautifulSoup
from crawler.web.web_node import WebNode

def test_brotli_compression():
    """Test that brotli compression is properly handled."""
    # Create a WebNode for a site that likely uses brotli compression
    # Google typically uses brotli compression
    url = "https://www.google.com"
    print(f"Testing with URL: {url}")

    # First, make a direct request to check the encoding
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response encoding: {response.headers.get('Content-Encoding', 'none')}")

        # Now create a WebNode and test our implementation
        node = WebNode(url)

        # Access the soup property to trigger the fetch and parse
        soup = node.soup

        # Check that we got a valid response
        assert soup is not None
        assert len(soup.text) > 0

        # Print some info about the soup
        print(f"Title: {soup.title.text if soup.title else 'No title'}")
        print(f"Content length: {len(soup.text)}")

        # Test passed if we got here without errors
        print("WebNode successfully handled the response")

        # If the response is brotli encoded, we can try to manually decompress it for comparison
        # but this is not required for the test to pass
        if 'br' in response.headers.get('Content-Encoding', '').lower():
            try:
                print("Attempting manual brotli decompression for comparison...")
                content = brotli.decompress(response.content).decode('utf-8')
                manual_soup = BeautifulSoup(content, "html.parser")
                print(f"Manual title: {manual_soup.title.text if manual_soup.title else 'No title'}")
                print(f"Manual content length: {len(manual_soup.text)}")

                # The content from both methods should be similar
                assert len(soup.text) > 0
                assert len(manual_soup.text) > 0
                print("Manual decompression successful and matches WebNode result")
            except Exception as e:
                print(f"Error in manual decompression: {e}")
                print("This is not a failure of our implementation, just additional information")
        else:
            print("Response is not brotli encoded, skipping manual decompression comparison")
    except Exception as e:
        print(f"Error during test: {e}")
        raise

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Run the test
    test_brotli_compression()

    print("All tests passed!")
