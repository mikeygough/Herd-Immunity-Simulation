from logger import Logger

if __name__ == "__main__":
    # Test your logger here
    logger = Logger('test-logger.txt')
    
    assert logger.file_name == 'test-logger.txt'