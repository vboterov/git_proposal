import argparse
import logging
from datetime import datetime

import pyspark.sql.functions as f
from pyspark.sql import Row
from pyspark.sql import SparkSession


class example_case:
    logger = logging.getLogger(__name__)

    def __init__(
        self,
        job_environment: str,
    ) -> None:
        self._job_environment = job_environment

    def main(self):
        df = self._spark.sql(
            f"SELECT traceability_no, dod, gender FROM fod_{self._job_environment}_deid.spot.fod_master_delivery_deid"
        )
        df = df.select("traceability_no", f.when(f.col("dod") > "2000-07-28"))
        df = df.filter((f.col("dod") > "2000-07-28") & (f.col("gender") == "M"))
        logging.info(
            f"""
                            ----------------------------------------------------------------------------------
             In the fod_master_delivery are {df.count()} man that dies aftes 28 of July 2000, searched on {datetime.now().strftime("%Y-%m-%d")}
                            -----------------------------------------------------------------------------------
        """
        )


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(name)s: %(processName)s %(module)s %(levelname)s: %(message)s",
        level=logging.INFO,
    )

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="fod_deid packaging delivery implementation"
    )
    parser.add_argument(
        "--job_environment", action="store", required=True, help="Desired environment "
    )

    args = parser.parse_args()

    example_case = example_case(job_environment=args.job_environment)

    example_case.main()
