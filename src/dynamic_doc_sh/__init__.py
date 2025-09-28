import argparse
from dynamic_doc_sh.generate_documentation import DocGenerator


def generate():
    """
    Function invoked to the command line, see pyproject.toml for more details.
    """

    parser = argparse.ArgumentParser(description="Documentation generator")

    parser.add_argument(
        "--script_path",
        type=str,
        required=True,
        help="The script to be documented",
    )
    parser.add_argument(
        "--doc_template_path",
        type=str,
        required=True,
        help="Jinja template to generate the documentation",
    )
    parser.add_argument(
        "--previous_hash_path",
        type=str,
        required=True,
        help="Hash of the previous documentation generated",
    )
    parser.add_argument(
        "--output_path",
        type=str,
        required=True,
        help="Where the output file will be",
    )
    parser.add_argument(
        "--debug", type=bool, default=False, help="Debug mode, used for testing"
    )

    args = parser.parse_args()

    generator = DocGenerator(
        script_path=args.script_path,
        doc_template_path=args.doc_template_path,
        previous_hash_path=args.previous_hash_path,
        output_path=args.output_path,
        debug=args.debug,
    )

    generator.generate()
