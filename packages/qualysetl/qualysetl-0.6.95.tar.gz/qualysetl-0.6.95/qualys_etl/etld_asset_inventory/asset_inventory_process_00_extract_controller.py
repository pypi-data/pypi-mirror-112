import re
import sqlite3
import time
import multiprocessing
from pathlib import Path
import os
import oschmod
import json
import shelve
import shutil
from qualys_etl.etld_lib import etld_lib_config as etld_lib_config
from qualys_etl.etld_lib import etld_lib_credentials as etld_lib_credentials
from qualys_etl.etld_lib import etld_lib_functions as etld_lib_functions
from qualys_etl.etld_lib import etld_lib_sqlite_tables as etld_lib_sqlite_tables
from qualys_etl.etld_lib import etld_lib_datetime as etld_lib_datetime
import qualys_etl.etld_asset_inventory.asset_inventory_process_00_extract as asset_inventory_extract

global host_list_records
global host_list_records_count
global host_list_get_scope_of_host_ids_sql
global asset_inventory_vm_processed_after
global asset_inventory_multi_proc_batch_size
global asset_inventory_concurrency_limit
global asset_inventory_batch_queue
global asset_inventory_limit_hosts
global spawned_process_info_list
global already_reported_spawned_process_info_status
global qualys_headers_multi_proc_dict
global xml_file_utc_run_datetime


# Create queue of batches to process.
# Each batch will be up to asset_inventory_multi_proc_batch_size.

def remove_old_files():
    if Path(etld_lib_config.asset_inventory_json_dir).name in 'asset_inventory_json_dir':
        os.makedirs(etld_lib_config.asset_inventory_json_dir, exist_ok=True)
        oschmod.set_mode(etld_lib_config.asset_inventory_json_dir, "a+rwx,g-rwx,o-rwx")
    # Remove old json files if they exist in asset_inventory_json_dir
    if Path(etld_lib_config.asset_inventory_json_dir).is_dir():
        if Path(etld_lib_config.asset_inventory_json_dir).name in 'asset_inventory_json_dir':
            count_files = 0
            for f in Path(etld_lib_config.asset_inventory_json_dir).glob('asset_inventory*.json'):
                count_files = count_files + 1
            etld_lib_functions.logger.info(f"Removing {count_files} old json files from dir: "
                                           f"{etld_lib_config.asset_inventory_json_dir}")

            files = Path(etld_lib_config.asset_inventory_json_dir).glob('asset_inventory*.json')
            try:
                for file in files:
                    file.unlink()
            except OSError as e:
                etld_lib_functions.logger.error(f"{e}")
                exit(1)
    try:
        if Path(etld_lib_config.asset_inventory_sqlite_file).is_file():
            etld_lib_functions.logger.info(f"Removing old sqlite file: {etld_lib_config.asset_inventory_sqlite_file}")
            Path(etld_lib_config.asset_inventory_sqlite_file).unlink()
        if Path(etld_lib_config.asset_inventory_shelve_file).is_file():
            etld_lib_functions.logger.info(f"Removing old shelve file: {etld_lib_config.asset_inventory_shelve_file}")
            Path(etld_lib_config.asset_inventory_shelve_file).unlink()
        if Path(etld_lib_config.asset_inventory_csv_file).is_file():
            etld_lib_functions.logger.info(f"Removing old csv file: {etld_lib_config.asset_inventory_csv_file}")
            Path(etld_lib_config.asset_inventory_csv_file).unlink()
    except Exception as e:
        etld_lib_functions.logger.error(f"{e}")
        exit(1)


# def extract_asset_inventory(host_ids, batch_number, xml_file_utc_run_datetime_arg):
#     asset_inventory_extract.multi_proc_host_ids = host_ids
#     asset_inventory_extract.qualys_headers_multi_proc_dict = qualys_headers_multi_proc_dict
#     asset_inventory_extract.multi_proc_batch_number = batch_number
#     asset_inventory_extract.xml_file_utc_run_datetime = xml_file_utc_run_datetime_arg
#     etld_lib_functions.logger.info(f"begin batch: {asset_inventory_extract.multi_proc_batch_number}")
#     asset_inventory_extract.main()
#     time.sleep(1)
#     etld_lib_functions.logger.info(f"end batch: {asset_inventory_extract.multi_proc_batch_number}")
#
#
# def get_asset_inventory_data(manager=None):
#     global asset_inventory_batch_queue
#     global spawned_process_info_list
#     global already_reported_spawned_process_info_status
#     global qualys_headers_multi_proc_dict
#     global xml_file_utc_run_datetime
#
#     qualys_headers_multi_proc_dict = manager.dict()
#     already_reported_spawned_process_info_status = []
#     spawned_process_info_list = []
#     hostid_batch_queue_size = asset_inventory_batch_queue.qsize()
#
#     etld_lib_functions.logger.info(f"asset_inventory host_ids per batch: "
#                                    f"{etld_lib_config.asset_inventory_multi_proc_batch_size}")
#     etld_lib_functions.logger.info(f"asset_inventory_batch_queue.qsize:  {hostid_batch_queue_size}")
#     etld_lib_functions.logger.info(f"user selected concurrency_limit:        "
#                                    f"{etld_lib_config.asset_inventory_concurrency_limit}")
#
#     xml_file_utc_run_datetime = etld_lib_datetime.get_utc_date()
#
#     if_exceeding_concurrency_reset_user_selected_concurrency_limit()
#
#     for batch in range(0, hostid_batch_queue_size, 1):
#         batch_data = asset_inventory_batch_queue.get()
#
#         spawned_process_info = \
#             multiprocessing.Process(target=extract_asset_inventory,
#                                     args=(batch_data['host_ids'],
#                                           batch_data['batch_number'],
#                                           xml_file_utc_run_datetime),
#                                     name=batch_data['batch_number'])
#         spawned_process_info_list.append(spawned_process_info)
#         test_child_processes_for_concurrency_max()
#         spawned_process_info.start()
#         test_for_errors_in_extracts(report_status=True)
#         test_child_processes_for_concurrency_max()
#
#     cleanup_remaining_processes()
#
#
# def cleanup_remaining_processes():
#     global asset_inventory_batch_queue
#
#     active_children = get_count_of_active_child_processes('batch_')
#     etld_lib_functions.logger.info(f"waiting for final active children: {multiprocessing.active_children()}")
#
#     while active_children > 0:
#         etld_lib_functions.logger.debug(f"waiting for final active children: {multiprocessing.active_children()}")
#         test_for_errors_in_extracts()
#         active_children = get_count_of_active_child_processes('batch_')
#
#     for spawned_process_info_final_status in spawned_process_info_list:
#         etld_lib_functions.logger.info(f"final job status spawned_process_info_status.exitcode: "
#                                        f"{spawned_process_info_final_status}")
#     asset_inventory_batch_queue = None
#
#
# def if_exceeding_concurrency_reset_user_selected_concurrency_limit():
#     global qualys_headers_multi_proc_dict
#     asset_inventory_extract.qualys_headers_multi_proc_dict = qualys_headers_multi_proc_dict
#     asset_inventory_extract.get_qualys_limits_from_asset_inventory()
#     user_selected_concurrency_limit = int(etld_lib_config.asset_inventory_concurrency_limit)
#
#     for key in qualys_headers_multi_proc_dict.keys():
#         qualys_concurrency_limit = int(qualys_headers_multi_proc_dict[key]['x_concurrency_limit_limit'])
#         etld_lib_functions.logger.info(f"Found {key} qualys header concurrency limit: {qualys_concurrency_limit}")
#
#         if user_selected_concurrency_limit >= qualys_concurrency_limit - 1:
#             etld_lib_config.asset_inventory_concurrency_limit = qualys_concurrency_limit - 1
#             etld_lib_functions.logger.info(f"resetting concurrency limit to: "
#                                            f"{etld_lib_config.asset_inventory_concurrency_limit}")
#         qualys_headers_multi_proc_dict.__delitem__(key)
#
#
# def get_count_of_active_child_processes(name='batch_'):
#     active_children = 0
#     for child in multiprocessing.active_children():
#         if str(child.__getattribute__('name')).__contains__(name):
#             active_children = active_children + 1
#     return active_children
#
#
# def test_child_processes_for_concurrency_max():
#     global qualys_headers_multi_proc_dict
#     etld_lib_functions.logger.info(f"test_child_processes_for_concurrency_max: {multiprocessing.active_children()}")
#     active_children = get_count_of_active_child_processes('batch_')
#     concurrency = int(etld_lib_config.asset_inventory_concurrency_limit)
#
#     while active_children >= concurrency:
#         etld_lib_functions.logger.debug(f"active_children: {active_children} "
#                                         f"limit: {concurrency} "
#                                         f"children: {multiprocessing.active_children()}")
#         test_for_errors_in_extracts()
#         active_children = get_count_of_active_child_processes('batch_')
#
#
# def terminate_program_due_to_error(terminate_process_info_status=None):
#     global spawned_process_info_list
#     global asset_inventory_batch_queue
#     global already_reported_spawned_process_info_status
#     # Error Occurred, Terminate all remaining jobs
#     etld_lib_functions.logger.error(f"terminate_process_info_status.exitcode: {str(terminate_process_info_status.exitcode)}")
#     etld_lib_functions.logger.error(f"terminate_process_info_status:          {terminate_process_info_status}")
#     etld_lib_functions.logger.error("Job exiting with error, please investigate")
#
#     for spawned_process_info_remaining in spawned_process_info_list:
#         if spawned_process_info_remaining.exitcode is None or spawned_process_info_remaining.exitcode != 0:
#             etld_lib_functions.logger.error(f"Terminating remaining process: {spawned_process_info_remaining}")
#             spawned_process_info_remaining.kill()
#             spawned_process_info_remaining.join()
#             spawned_process_info_remaining.close()
#             etld_lib_functions.logger.error(f"Status after 'terminate, join, close': {spawned_process_info_remaining}")
#     # Empty Queue
#     etld_lib_functions.logger.error(f"cancel remaining batches in queue: {asset_inventory_batch_queue.qsize()}")
#     for batch in range(0, asset_inventory_batch_queue.qsize(), 1):
#         empty_out_queue = asset_inventory_batch_queue.get()
#     etld_lib_functions.logger.error(f"batches remaining in queue: {asset_inventory_batch_queue.qsize()}")
#     # ALL JOB STATUS
#     for spawned_process_info_final_status in spawned_process_info_list:
#         etld_lib_functions.logger.error(f"final job status spawned_process_info_status.exitcode: {spawned_process_info_final_status}")
#     exit(1)
#
#
# def test_for_errors_in_extracts(report_status=False):
#     global spawned_process_info_list
#     global asset_inventory_batch_queue
#     global already_reported_spawned_process_info_status
#
#     time.sleep(1)
#     for spawned_process_info_status in spawned_process_info_list:
#         if spawned_process_info_status.exitcode is not None:
#             if spawned_process_info_status.exitcode > 0:
#                 # Error Occurred, Terminate all remaining jobs
#                 terminate_program_due_to_error(terminate_process_info_status=spawned_process_info_status)
#             elif (spawned_process_info_status.exitcode == 0 and report_status is True) and \
#                     not already_reported_spawned_process_info_status.__contains__(spawned_process_info_status.pid):
#                 # Report exit status only one time, keep track of already reported status.
#                 already_reported_spawned_process_info_status.append(spawned_process_info_status.pid)
#                 etld_lib_functions.logger.info(f"job completed spawned_process_info_status.exitcode: {spawned_process_info_status}")
#             elif spawned_process_info_status.exitcode < 0:
#                 # Odd error.  Report and quit.
#                 etld_lib_functions.logger.error(f"odd negative spawned_process_info_status.exitcode: {spawned_process_info_status}")
#                 etld_lib_functions.logger.error(f"spawned_process_info_status: "
#                                                 f"{spawned_process_info_list}")
#                 exit(1)
#
#
# def prepare_host_id_batches_for_asset_inventory_extract(manager=None):
#     global asset_inventory_batch_queue
#     global asset_inventory_vm_processed_after
#
#     asset_inventory_batch_queue = manager.Queue()
#     batch_number = 1
#     batch_size_counter = 0
#     batch_size_max = int(etld_lib_config.asset_inventory_multi_proc_batch_size)
#     if batch_size_max > 750:
#         etld_lib_functions.logger.info(f"reset batch_size_max to 750.")
#         etld_lib_functions.logger.info(f" user select batch_size_max was {batch_size_max}.")
#         batch_size_max = 750
#         etld_lib_config.asset_inventory_multi_proc_batch_size = 750
#
#     host_id_list = []
#     for ID, DATETIME in host_list_records:
#         if batch_size_counter >= int(batch_size_max):
#             # create new batch
#             asset_inventory_batch_queue.put({'batch_number': f"batch_{batch_number:06d}", 'host_ids': host_id_list})
#             host_id_list = []
#             batch_number = batch_number + 1
#             batch_size_counter = 0
#         host_id_list.append(ID)
#         batch_size_counter = batch_size_counter + 1
#
#     if len(host_id_list) > 0:
#         asset_inventory_batch_queue.put({'batch_number': f"batch_{batch_number:06d}", 'host_ids': host_id_list})
#     else:
#         etld_lib_functions.logger.info(f"There were no hosts found with vm_processed_after date of: "
#                                        f"{asset_inventory_vm_processed_after}")
#         etld_lib_functions.logger.info(f"Please select another date and rerun.  No errors, exiting with status of zero.")
#         exit(0)
#
#
# def get_scope_of_host_ids_from_host_list():
#     global host_list_records
#     global host_list_records_count
#     global host_list_get_scope_of_host_ids_sql
#     global asset_inventory_vm_processed_after
#     global asset_inventory_limit_hosts
#
#     asset_inventory_limit_hosts = etld_lib_config.asset_inventory_limit_hosts
#     if etld_lib_datetime.is_valid_qualys_datetime_format(etld_lib_config.asset_inventory_vm_processed_after):
#         vm_processed_after = etld_lib_config.asset_inventory_vm_processed_after
#         vm_processed_after = re.sub("T", " ", vm_processed_after)
#         vm_processed_after = re.sub("Z", "", vm_processed_after)
#         asset_inventory_vm_processed_after = vm_processed_after
#     else:
#         etld_lib_functions.logger.error(f"error vm_processed_after: {etld_lib_config.asset_inventory_vm_processed_after} ")
#         exit(1)
#     #
#     #  f"WHERE LAST_VM_SCANNED_DATE > datetime('{vm_processed_after}') "
#     #  Qualys has internal algorithm for vm_processed_after.  Trust host list to pull all vm_processed after
#     #  and select all assets where LAST_VM_SCANNED_DATE is not "" or NULL.
#     #
#     sql_statement = f"SELECT t.ID, t.LAST_VM_SCANNED_DATE FROM Q_Host_List t " \
#                     f'WHERE LAST_VM_SCANNED_DATE is not "" or NULL ' \
#                     f"ORDER BY LAST_VULN_SCAN_DATETIME DESC limit {asset_inventory_limit_hosts}"
#
#     host_list_get_scope_of_host_ids_sql = sql_statement
#
#     try:
#         conn = sqlite3.connect(etld_lib_config.host_list_sqlite_file, timeout=20)
#         cursor = conn.cursor()
#         cursor.execute(sql_statement)
#         host_list_records = cursor.fetchall()
#         host_list_records_count = len(host_list_records)
#         cursor.close()
#         conn.close()
#     except Exception as e:
#         etld_lib_functions.logger.error(f"error sqlite db: {etld_lib_config.host_list_sqlite_file}")
#         etld_lib_functions.logger.error(f"exception: {e}")
#         exit(1)
#     finally:
#         if conn:
#             conn.close()


def start_msg_get_asset_inventory_data():
    etld_lib_functions.logger.info(f"start")


def end_msg_get_asset_inventory_data():
    etld_lib_functions.logger.info(f"host_list get_scope_of_host_ids sql: {host_list_get_scope_of_host_ids_sql}")
    etld_lib_functions.logger.info(f"host_list sqlite file: {etld_lib_config.host_list_sqlite_file}")
    etld_lib_functions.logger.info(f"count host_list host id: {len(host_list_records):,}")
    etld_lib_functions.logger.info(f"end")


def get_next_batch(json_file=None):
    batch_info = {}
    with open(json_file, "r", encoding='utf-8') as read_file:
        with shelve.open(str(etld_lib_config.asset_inventory_temp_shelve_file), flag='n') as shelve_database_temp:
            shelve_database_temp = json.load(read_file)
            if 'hasMore' in shelve_database_temp.keys():
                batch_info = {'responseCode': shelve_database_temp['responseCode'],
                              'count': shelve_database_temp['count'],
                              'hasMore': shelve_database_temp['hasMore'],
                              'lastSeenAssetId': shelve_database_temp['lastSeenAssetId'],
                              }
    return batch_info


def get_asset_inventory_data():
    global qualys_headers_multi_proc_dict
    start_msg_get_asset_inventory_data()
    utc_datetime = etld_lib_datetime.get_utc_date()
    qualys_headers_multi_proc_dict = {}
    batch_info = {'hasMore': '1', 'lastSeenAssetId': 0}
    has_more_records = '1'
    batch_number = 0
    while has_more_records == '1':
        batch_number = batch_number + 1
        batch_number_str = f'batch_{batch_number:06d}'
        asset_inventory_extract.asset_inventory_extract(
            asset_last_updated=etld_lib_config.asset_inventory_asset_last_updated,
            last_seen_assetid=str(batch_info['lastSeenAssetId']),
            utc_datetime=utc_datetime,
            batch_number=batch_number_str,
            proc_dict=qualys_headers_multi_proc_dict)
        batch_info = get_next_batch(json_file=asset_inventory_extract.json_file)
        etld_lib_functions.logger.info(f"batch_info: {batch_info}")
        if 'hasMore' in batch_info.keys():
            has_more_records = str(batch_info['hasMore'])
        else:
            etld_lib_functions.logger.error("Error downloading records")
            etld_lib_functions.logger.error(f"batch_info: {batch_info}")
            exit(1)
        if batch_number_str in qualys_headers_multi_proc_dict.keys():
            x_ratelimit_remaining = qualys_headers_multi_proc_dict[batch_number_str]['x_ratelimit_remaining']
            if int(x_ratelimit_remaining) < 100:
                # Sleep for 5 minutes and run next.
                etld_lib_functions.logger.warning(f"x_ratelimit_remaining is less than 100. "
                                                  f"Sleeping 5 min.  batch_info: {batch_info}, "
                                                  f"header_info: {qualys_headers_multi_proc_dict[batch_number_str]}")
                time.sleep(300)


def main():
    remove_old_files()
    get_asset_inventory_data()


if __name__ == "__main__":
    etld_lib_functions.main(my_logger_prog_name='asset_inventory_extract_controller')
    etld_lib_config.main()
    etld_lib_credentials.main()
    main()

