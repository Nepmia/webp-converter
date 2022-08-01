import sys
import argparse
import os
import logging as log
from PIL import Image

from helpers import verify_logs, create_log_folder, log_base_dir, basic_answers, basic_yes_default, user_prompt, parser

if not verify_logs():
    create_log_folder()

log.basicConfig(
    encoding="utf-8",
    level=log.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        log.FileHandler(f"{log_base_dir}/converter.log"),
        log.StreamHandler(sys.stdout),
    ],
    datefmt="%Y-%m-%d %H:%M:%S",
)


def convert_images(path_to_exec:str, source_extension:str, target_extension:str, always_overwrite:bool):
    
    file_list = None
    
    log.info("Trying to list given directory.")
    try:
        file_list = os.listdir(path_to_exec)
    except FileNotFoundError:
        log.critical("FileNotFoundError, verify the given path.")
        sys.exit()
    

    if file_list:
        log.info("Folder listed, converting images.")
        for file in file_list:
            if file.endswith(source_extension):

                raw_file_name = file.replace(f'.{source_extension}', '')

                # Defaults to true and will change with prompt
                answer = True

                if file.endswith(target_extension) and not always_overwrite:
                    answer = user_prompt(basic_answers, "File already exist, overwrite?", basic_yes_default, "yes")

                if answer:
                    log.info(f"Converting {file} to {raw_file_name}.{target_extension}")
                    image = Image.open(os.path.join(path_to_exec, file))
                    image.save(f"{path_to_exec}/{raw_file_name}.{target_extension}")
                else:
                    log.warning(f"User denied overwriting of file {raw_file_name}.{target_extension}, skipping it.")
                
    log.info("Job finished.")


if __name__ == "__main__":
    # Define basic args
    parser.add_argument("path_to_exec", help="Path to the folder that contains the image we want to convert")
    parser.add_argument("source_extension", help="Extension of the file that needs to be converted (can be a list)")
    parser.add_argument("target_extension", help="Extension of the newly created files (can be a list)")
    parser.add_argument("-o","--overwrite", required=False, default=False, help="Option to always overwrite files", action="store_true")
    
    # Parse the args
    args = parser.parse_args()

    log.info("Starting process.")
    log.debug(f"got args: {args}")

    # Launch the conversion
    convert_images(args.path_to_exec, args.source_extension, args.target_extension, args.overwrite)

