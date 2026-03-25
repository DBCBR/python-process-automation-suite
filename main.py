"""
Main CLI entry point for Python Process Automation Suite.

Usage:
    python main.py --pipeline cnpj --input "12.345.678/0001-90"
    python main.py --pipeline cnpj --file "data.txt"
    python main.py --list

Examples:
    python main.py --pipeline cnpj --input "11.222.333/0001-81"
    python main.py --pipeline cnpj --file cnpjs.txt
    python main.py --list
"""

import argparse
import sys
from typing import Optional

from automation.pipelines.cnpj_pipeline import CNPJPipeline
from automation.utils.logger import get_logger
from config.settings import settings


logger = get_logger(__name__)


AVAILABLE_PIPELINES = {
    "cnpj": {
        "class": CNPJPipeline,
        "description": "CNPJ validation and company data enrichment pipeline",
    }
}


def run_cnpj_pipeline(
    input_data: Optional[str] = None,
    file_path: Optional[str] = None,
) -> None:
    """
    Execute CNPJ pipeline.

    Args:
        input_data: Single CNPJ or list of CNPJs
        file_path: Path to file containing CNPJs or text
    """
    logger.info("Initializing CNPJ Pipeline")

    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text_content = f.read()
            pipeline = CNPJPipeline(text_source=text_content)
            logger.info(f"Loaded text from {file_path}")
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            sys.exit(1)
    else:
        # Single CNPJ or comma-separated list
        cnpj_list = [c.strip() for c in input_data.split(",")] if input_data else []
        pipeline = CNPJPipeline(cnpj_list=cnpj_list)

    result = pipeline.run()

    logger.info(f"Pipeline completed: {result['status']}")
    logger.info(f"Processed: {result['total_processed']} records")

    if result["results"]:
        logger.info(f"Retrieved data for {len(result['results'])} CNPJs")


PIPELINE_RUNNERS = {
    "cnpj": run_cnpj_pipeline,
}


def run_pipeline(
    name: str, input_data: Optional[str], file_path: Optional[str]
) -> None:
    """Run selected pipeline from registry."""
    runner = PIPELINE_RUNNERS.get(name)
    if runner:
        runner(input_data=input_data, file_path=file_path)
        return

    logger.error(f"Pipeline '{name}' not implemented")
    sys.exit(1)


def list_pipelines() -> None:
    """List all available pipelines."""
    print("\n📦 Available Pipelines:\n")
    for name, info in AVAILABLE_PIPELINES.items():
        print(f"  • {name.upper()}")
        print(f"    Description: {info['description']}")
        print()


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Python Process Automation Suite - CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --pipeline cnpj --input "12.345.678/0001-90"
  python main.py --pipeline cnpj --file "cnpjs.txt"
  python main.py --list
        """,
    )

    parser.add_argument(
        "--pipeline",
        type=str,
        help="Pipeline to execute",
        choices=list(AVAILABLE_PIPELINES.keys()),
    )
    parser.add_argument(
        "--input",
        type=str,
        help="Input data (CNPJ or comma-separated list)",
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Input file path",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available pipelines",
    )

    args = parser.parse_args()

    logger.info(f"Starting application - Environment: {settings.ENVIRONMENT}")

    if args.list:
        list_pipelines()
        return

    if not args.pipeline:
        parser.print_help()
        sys.exit(1)

    if not args.input and not args.file:
        logger.error("Either --input or --file is required")
        parser.print_help()
        sys.exit(1)

    run_pipeline(name=args.pipeline, input_data=args.input, file_path=args.file)


if __name__ == "__main__":
    main()
