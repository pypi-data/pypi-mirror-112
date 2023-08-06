from bullets import logger

if __name__ == "__main__":
    # Default level is info
    #logger.set_log_level("DEBUG")
    #logger.set_log_level("ERROR")

    logger.error("This is an error")
    logger.warning("This is a warning")
    logger.info("This is an info")
    logger.debug("This is a debug")