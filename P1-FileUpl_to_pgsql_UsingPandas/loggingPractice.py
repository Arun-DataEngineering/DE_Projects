import logging;

logging.basicConfig(
                    filename = "D:\\Python_DE\\DE_Projects\\logging_log.log",
                    level=logging.DEBUG,
                    format = '%(asctime)s %(levelname)s %(message)s'
);

try:
    logging.debug("Debug Message")
    logging.info("Info Message")
    logging.warning("Warning Message")
    logging.error("Error Message")
    logging.critical("Critical Message")
    num = 10/0;
except Exception as a:
    print ("Exception Occoured : ",a)

finally:
    logging.info("Pipeline Execution Finished")