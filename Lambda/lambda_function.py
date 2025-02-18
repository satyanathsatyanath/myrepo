# Import basic python packages
from utils.image_utils.Image_Summaries_Open_AI_V2 import (get_Summaries_For_Table_Image_Charts,
                                                          has_png_images)
import time
import datetime
from utils.misc_utils.metadata_extractor import MetadataExtractor
from constant.constants import model_config, classification_config
from constant.constants import classification_config
from utils.utils_IDA_ver_2_updated_cache_pipeline import (
    document_processing,
    new_file_pkl_db_creation,
    Answer_Pre_Processor,
    Exisiting_file_pipeline,
    DirectoryCreator,
    write_query_response_to_file,
    save_query_response_to_csv,
    merging_pkl_db,
    backup_files,
    initialize_pipeline,
    master_pkl_initial_creation,
    extract_values,
    node_creator

)
from configuration.folder_config import (
    folder_path_pdf,
    output_folder,
    folder_path_html,
    vector_store,
    folder_path_pkl,
    directories_to_create,
    report_file_path,
    all_files_path,
    text_summary_folder_path,
    temp_text_file_path
)


from main_IDA_ver_2_updated import llm, embed_model
from utils.image_utils.PDF_Extraction_V2 import pdf_Extraction_Using_Unstructure
from utils.image_utils.KB_text_preprocess import text_preprocess_for_kbase, extract_between_keywords, extract_text_blocks
from llama_index.core import Settings
from llama_index.core import SimpleDirectoryReader
import pickle
from keras.models import load_model
import keras
# import torch
import tensorflow as tf
# from logger import setup_logging, delete_old_log_files, log_dir
from exception import Custom_Exception
# from flask_cors import CORS
import json
import traceback
import sys
# import logging
from pathlib import Path
import shutil
import csv
# from flask import (
#     Flask,
#     request,
#     redirect,
#     url_for,
#     send_from_directory,
#     send_file,
#     jsonify,
#     flash,
#     render_template,
#  )
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

# Import Custom logger and expections, constant and config

# Import Require base packages

# Import from llama-index library
# from PDF_Extraction_V1 import layout_analysis_unstructured_pymupdf_V4
# from image_summaries_with_open_ai import get_summaries_for_table_image_charts


# from utils.misc_utils.id_from_file_name import key_searcher

# Initialising Logger
# setup_logging()

# Setting Default paramters
Settings.llm = llm
Settings.embed_model = embed_model

# #----------------------gpu allocation-------------------------------------------------


gpus = tf.config.list_physical_devices("GPU")
if gpus:
    # Restrict TensorFlow to only allocate 10GB of memory on the first GPU
    try:
        tf.config.set_logical_device_configuration(
            gpus[0], [tf.config.LogicalDeviceConfiguration(memory_limit=10024)]
        )
        logical_gpus = tf.config.list_logical_devices("GPU")
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Virtual devices must be set before GPUs have been initialized
        print(e)

# Load the model specifying only GPU 0
# with tf.device(classification_config.TF_DEVICE):
#     model = load_model(classification_config.CLASSIFICATION_MODEL)
# # -------------------------------------------------------------------------------------

# app = Flask(__name__)
# CORS(app)

query_engine_output = None  # Initialize to None
file_name = ""
print("Starting Pdf_Doc_Chat Application..")
# logging.info("Starting Pdf_Doc_Chat Application....")
# Creation of all folder --> function in utils.py --> folders from folder_config.py
dir_creator = DirectoryCreator(*directories_to_create)
dir_creator.create_directories()
Master_pkl_path = os.path.join(folder_path_pkl, "Master_nodes.pkl")

# Merged_pkl_path=os.path.join(folder_path_pkl, "Merge_nodes.pkl")
Master_Vector_store_path = os.path.join(
    vector_store + "/" + "Master_Vector_Store")

Master_vector_index_name = "/tmp/PDF_uploads_integration/Vector_Store/Master_Vector_Store/index_store.json"
# Merged_vector_store_path=os.path.join(vector_store + "/" + "Merge_Vector_Store")
# Merge_vector_index_name = "Merge_index"

# Scenarios covered for fresh start when no files exist in knowledge base  
if os.path.exists(Master_pkl_path):
    pass
else:
    #create master pkl file with empty text - Dummy mater_pkl and master_vector_DB creation
    master_pkl_initial_creation(temp_text_file_path,Master_pkl_path,Master_Vector_store_path,Master_vector_index_name)



# Master Data Creation

# master_data_creation(all_files_path,Master_pkl_path,Master_Vector_store_path,Master_vector_index_name)
# logging.info("Entering initialize_pipeline")
print("Entering initialize_pipeline")
initialize_pipeline(all_files_path, Master_pkl_path,
                    Master_Vector_store_path, Master_vector_index_name)
# logging.info("Exisitng initialize_pipeline")
print("Existing initialize_pipeline")


# @app.route("/knowledge_base_doc_chat", methods=["POST"])
def lambda_handler(event,context):
    global query_engine_output
    # logging.info("Entered into pdf_doc_chat function from app_intergration.py")
    data = json.loads(event['body'])
    query = data["Question"]
    # logging.info("Exited from pdf_doc_chat function from app_intergration.py")
    return output(query, query_engine_output)
    # query = request.form.get('query', '')


# @app.route("/file_upload_to_knowledge_base", methods=["POST"])
def file_path():
    # logging.info("Entered into file_upload function from app_integration.py")
    global query_engine_output, Master_pkl_path, Master_Vector_store_path, Master_vector_index_name
    global file_name
    global text_file_path
    # file = request.files['file']
    # print('file', file.filename)

    # json_data = request.form.get('json')
    # filename_data = json.loads(json_data)

    # # Access the filename attribute
    # filename = filename_data['filename']
    # print('filename_from_json_data', filename)

    # to test on postaman
    # file = request.files["file"]
    print("file", file.filename)

    # if os.path.exists(folder_path_pdf):
    #     shutil.rmtree(folder_path_pdf)

    # # Creation of all folder --> function in utils.py --> folders from folder_config.py
    # dir_creator = DirectoryCreator(*directories_to_create)
    # dir_creator.create_directories()

    # For testing on UI

    # if filename == '':
    #         return "No selected file"

    # if file:
    #         file_name, file_extension = os.path.splitext(filename)
    #         print("File name:", file_name)
    #         print("File extension:", file_extension)
    #         pdf_file_path = os.path.join(folder_path_pdf, filename)
    #         print("PDF FILE PATH :::",pdf_file_path)
    #         file.save(pdf_file_path)
    #         logging.info(f"File is saved to : {pdf_file_path}")

    # For testing over postman
    if file.filename == "":
        return "No selected file"

    if file:
        file_name, file_extension = os.path.splitext(file.filename)
        print("File name:", file_name)
        print("File extension:", file_extension)
        pdf_file_path = os.path.join(folder_path_pdf, file.filename)
        print("Actual FILE PATH :::", pdf_file_path)
        file.save(pdf_file_path)
        # logging.info(f"File is saved to : {pdf_file_path}")

        if '_' in file_name:
            device_name = "_".join(file_name.split('_')[1:])
        else:
            device_name = file_name

        print('device name -> : ',device_name)

        print("Checking if file already exists")
        # logging.info("Checking if file already exists")

        folder_path_pkl_check = os.path.join(
            folder_path_pkl, file_name + ".pkl")

        Vector_store_check_path = os.path.join(vector_store + "/" + file_name)

        vector_index_name = file_name + "_index"
        sections_wise_text_blocks_text = {} 
        
        if all(map(os.path.exists, [folder_path_pkl_check])):
            # logging.info("All Files are present")
            print("All Files are present")

            # merging_pkl_db(folder_path_pkl_check,
            #             Master_pkl_path,
            #             Master_Vector_store_path,
            #             Master_vector_index_name)
            # backup_files(folder_path_pdf, all_files_path)

            # logging.info("File fetched successfully")
            return json.dumps("File fetched successfully")

        else:
            if file_extension == '.pdf':
                # logging.info("PDF Analysis is running in file_path function")
                print("PDF Analysis is running")

                start_Time = time.time()
                print("output_folder", output_folder)
                print('getting pdf text using unstructured')
                imgs_path, tables_path, pages_text_path, full_pages_text, file_name_without_extension, first_page_text = pdf_Extraction_Using_Unstructure(
                    pdf_file_path, output_folder)

                full_pages_text = text_preprocess_for_kbase(full_pages_text,device_name)
                print('getting pdf text using unstructured is Completed')

                end_Time = time.time()

                print(
                    "Pdf extraction done succuessfully. Time taken for executing total pdf extraction ----->"
                    + str(datetime.timedelta(seconds=(end_Time - start_Time)))
                )
                # logging.info("""Pdf extraction done succuessfully. 
                                # Time taken for executing total pdf extraction ->"""
                            #  + str(datetime.timedelta(seconds=(end_Time - start_Time))))

                print(
                    'getting summaries for images, charts and tables are started using open ai')
                # logging.info(
                #     'getting summaries for images, charts and tables are started using open ai')

                sections_wise_text = ""

                if imgs_path is not None:
                    # new_text_html = None
                    if has_png_images(imgs_path, tables_path):
                        try:
                            print("Getting Image summaries - Running ...")
                            list2 = get_Summaries_For_Table_Image_Charts(full_pages_text,
                                                                         imgs_path,
                                                                         tables_path,
                                                                         classification_config.OPENAI_API_KEY)
                            all_text_pdf_summary = '\n\n'.join(list2)
                            # new_text_html = f'<html><body><pre>{all_text_pdf_summary}</pre></body></html>'

                            sections_wise_text = all_text_pdf_summary

                            text_file_path = f"{text_summary_folder_path}/{file_name}.txt"

                            print("@" * 50)
                            print("text_file_path", text_file_path)
                            # logging.info("Exited from Image analysis")
                            # Write the HTML code to a file with .html extension
                            with open(text_file_path, "w") as file:
                                file.write(all_text_pdf_summary)
                                file.close()
                            # logging.info("Text file Summaries with table and images are saved")
                        except Exception as e:
                            print(e)
                            print('Error while getting image summaries.')
                    else:
                        print('No images - No summary')
                        text_file_path = f"{text_summary_folder_path}/{file_name}.txt"
                        sections_wise_text = full_pages_text
                        with open(text_file_path, "w") as file:
                            file.write(full_pages_text)
                            file.close()
                        # logging.info("Plain extracted text is saved in file")

                        # new_text_html = f'<html><body><pre>{full_pages_text}</pre></body></html>'

                    # save_text_to_file(str(new_text_html),f'{pages_text_path}/{file_name_without_extension}.html')
                    print('successful overall process.')
                else:
                    print('error in get text from unstructured')

                # get dict wise blocks of description, benifits, ...
                sections_wise_text_blocks_text_dictionary = extract_text_blocks(sections_wise_text)
                # return sections_wise_text_blocks_text_dictionary
                list_of_texts=extract_values(sections_wise_text_blocks_text_dictionary) 
                nodes=node_creator(list_of_texts,file_name)
                pickle.dump(nodes, open(folder_path_pkl_check, "wb"))
                # print('sections_wise_text_bloextract_valuescks_text',sections_wise_text_blocks_text_dictionary)
                # print("list_of_texts",list_of_texts)
                # return [sections_wise_text_blocks_text_dictionary , list_of_texts]
                # print("Dict and list is created")                
            if file_extension == '.txt':
                # text_file_path = f"{text_summary_folder_path}/{file_name}.txt"
                # text_file_path = f"{text_summary_folder_path}/{file_name}.txt"
                # print("file.filename",file.filename)
                # pdf_file_path_for_text = os.path.join(folder_path_pdf, file.filename)
                # print("PDF FILE PATH :::", pdf_file_path_for_text)
                # file.save(pdf_file_path_for_text)
                # # file.save(text_file_path)
                # logging.info(f"File is saved to : {pdf_file_path_for_text}")
                print("file.filenameok", file.filename)
                text_file_path = os.path.join(folder_path_pdf, file.filename)
                print("TEXT FILE PATH :::", text_file_path)
                file.save(text_file_path)
                # file.save(text_file_path)
                # logging.info(f"File is saved to : {text_file_path}")

        
        # --------------------  Q&A  ----------------------------------------------------------------------------------------------------------------
        print("---Entry point for Q&A----")
        # logging.info("Entered into document_processing function from app_integration.py")
        # output_html_file_path = folder_path_html + "/" + file_name + ".html"
        # text_file_path = f"{text_summary_folder_path}/{file_name}.txt"
        # output_html_file_path = document_processing(
        #     output_html_file_path, text_file_path)


        # logging.info(
        #     "Exited from document_processing function from app_integration.py")

        print("**************************************^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        # query_engine_output=pre_processing(output_html_file_path,vector_index_name)
        # logging.info("Entered into pre_processing function from app_integration.py")
        print("Entered into pre_processing function from app_integration.py")

        # new_file_pkl_db_creation(output_html_file_path, vector_index_name, Vector_store_check_path,
        #                          folder_path_pkl_check)

        merging_pkl_db(folder_path_pkl_check, Master_pkl_path,
                       Master_Vector_store_path, Master_Vector_store_path)
        # logging.info("node are merged with Master Pickle file")
        print("node are merged with Master Pickle file @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        backup_files(folder_path_pdf, all_files_path)
        query_engine_output=Exisiting_file_pipeline(
            Master_pkl_path,Master_Vector_store_path,Master_vector_index_name)
    # logging.info("Exited from pre_processing function from app_integration.py")
    print("Exited from pre_processing function from app_integration.py")

    # logging.info("Exited from doc_chat function from app_integration.py")


    if query_engine_output is None:
        query_engine_output=Exisiting_file_pipeline(
            Master_pkl_path,Master_Vector_store_path,Master_Vector_store_path)

    print("File uploaded successfully")
    # logging.info("File uploaded successfully")
    return json.dumps("File uploaded successfully")

    # if all(map(os.path.exists, [Master_pkl_check, Master_Vector_store_check_path])):
    #     logging.info("All Files are present")
    #     print("All Files are present")

    
query_engine_output=Exisiting_file_pipeline(
            Master_pkl_path,Master_Vector_store_path,Master_vector_index_name)
# logging.info("File ready for Q&A")
print("query_engine_output", query_engine_output)


# @app.errorhandler(RuntimeError)
# def handle_cuda_out_of_memory_error(error):
#     logging.info(
#         "Entered into handle_cuda_out_of_memory_error with main query ")
#     if "CUDA out of memory" in str(error):
#         return (jsonify({
#             "Memory Error": "Oops, it seems like internal memory error. Please contact your provider for further assistance"
#         }), 500,)
#     else:
#         return (jsonify({
#             "Error": "Oops, it seems like an error has occured. Please contact your provider for further assistance"
#         }), 500,)


def output(main_query, query_engine_output):
    global file_name
    print("query_engine_output_2", query_engine_output)
    output_text = ""  # Initialize to an empty string or a default value
    key = None
    print("query_engine_output is *******", query_engine_output)
    try:
        # logging.info("Entered into output function with main query ")
        if query_engine_output:
            print('$'*80)
            print("query engine_output from app.py", query_engine_output)
            print('$'*80)

            # response from query engine retriever object
            answer = query_engine_output.query(main_query).response
            
            print('$'*80)
            print("query engine_output.query(main_query) from app.py",
                  query_engine_output.query(main_query))
            print('$'*80)

            # metadata object cration
            # metadata_extractor = MetadataExtractor(answer)

            # getting file name from the response metadata
            # doc_file_name = metadata_extractor.get_metadata_key('file_name')

            # getting key i.e id from json data fro respective file name
            # key = key_searcher.search_key_by_file_name(doc_file_name)

            # Response preprocessor
            output_text = f" {Answer_Pre_Processor.process_answer(answer)} "

            # logging.info("Existed output function with main query-if")
            # logging.info(f" Query : {main_query} \n\n Response: {output_text}  ")
        else:
            output_text = """Oops, There is no output available for your query at the moment. 
            Kindly try uploading the file again and patiently await the confirmation message stating 'File uploaded successfully'. 
            *NOTE*- Upload may take a bit longer, especially if the document contains a large number of pages and contains many images."""

            # logging.info("Existed output function with main query-else")
            # logging.info(f" Query : {main_query} \n\n Response: {output_text}  ")
    except RuntimeError as e:
        raise e

    except Exception as e:
        text = f"Error: {str(e)}"
        # logging.info(f" Exception Raised  : {text}")
        raise Custom_Exception(e, sys) from e

    write_query_response_to_file(
        main_query, output_text, report_file_path, file_name)
    save_query_response_to_csv(
        main_query, output_text, report_file_path, file_name)

    # torch.cuda.empty_cache()
    # delete_old_log_files(log_dir)
    # logging.info(f"Output is Jsonified in chatbot and Cache are Emptied ")

    # Create a JSON response containing output_text and key
    response_data = {
        'response': output_text,
        # 'id': key
    }

    return json.dumps(response_data)
    # return jsonify(output_text)

    # remove input file
    os.remove(pdf_file_path)
    # remove temporary text file for initialization
    os.remove(temp_text_file_path)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=7194, debug=False)
