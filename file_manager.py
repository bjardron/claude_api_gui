import os
import concurrent.futures

class FileManager:
    def __init__(self):
        self.staged_files = []
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

    def filter_code_files(self, directory, allowed_extensions):
        code_files = []
        for root, dirs, files in os.walk(directory):
            # Exclude directories starting with a dot (like .git)
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for file in files:
                file_path = os.path.join(root, file)
                if any(file_path.endswith(ext) for ext in allowed_extensions):
                    code_files.append(file_path)
        return code_files

    def clear_staged_files(self):
        self.staged_files.clear()
