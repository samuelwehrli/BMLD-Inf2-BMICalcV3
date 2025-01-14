import os, requests, copy
from requests.auth import HTTPBasicAuth

class SwitchDrive:
    def __init__(self, username: str, passcode: str, root_path, 
                 webdav_url: str = 'https://drive.switch.ch/remote.php/webdav/'):
        """Initialize a SwitchDrive client for interacting with SWITCHdrive WebDAV storage.

        Args:
            username: SWITCHdrive username for authentication
            passcode: SWITCHdrive password or access token
            root_path: Base directory path to use as root for all operations
            webdav_url: WebDAV endpoint URL, defaults to SWITCHdrive production URL
        """
        self.webdav_url = webdav_url.rstrip('/') # strip all trailing slashes
        self.root_path = root_path.strip('/') if root_path else '' # strip all slashes
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(username, passcode)

    def get_subfolder_drive(self, subfolder_name: str):
        drive = copy.copy(self)
        drive.root_path = f"{self.root_path}/{subfolder_name.strip('/')}"
        return drive

    def _full_path(self, path: str, root_path: str = None) -> str:
        """Build the complete WebDAV URL for a given path.

        Combines the base WebDAV URL with root path and provided path, handling slashes appropriately.

        Args:
            path: Relative path to append after root path
            root_path: Optional override for instance root_path

        Returns:
            Complete WebDAV URL with all path components
        """
        # Remove leading slash if present to avoid double slashes
        path = path.strip('/')
        if root_path is None:
            root_path = self.root_path
        else:
            root_path = root_path.strip('/')
        
        # Combine root_path with given path, ensuring single slash between parts
        if len(root_path) > 0:
            full_path = f"{root_path}/{path}" 
        else:
            full_path = path
                
        # Construct full URL
        return f"{self.webdav_url}//{full_path}"

    def create_folder(self, remote_path: str, root_path: str = None):
        full_path = self._full_path(remote_path, root_path)
        response = self.session.request('MKCOL', full_path)
        return response.ok or response.status_code == 405  # 405 Method Not Allowed means it already exists

    def ensure_folder_exists(self, full_file_path: str):
        """Create all parent directories for a given file path.

        Splits the path into components and creates each directory level if missing.

        Args:
            full_file_path: Complete file path whose directories should exist
        
        Raises:
            Exception: If directory creation fails
        """
        webdav_folder_list = full_file_path.split('//')[-1].split('/')[:-1]


        for ii_part, _ in enumerate(webdav_folder_list):
            folder_path = '/'.join(webdav_folder_list[:ii_part+1])
            if not self.exists(folder_path, root_path=''):
                ok = self.create_folder(folder_path, root_path='')
                if not ok:
                    raise Exception(f"Failed to create directory {folder_path}")

    def delete_file(self, remote_path: str) -> bool:
        """Delete a file from SWITCHdrive.

        Args:
            remote_path: Path of file to delete

        Returns:
            True if deletion succeeded, False otherwise
        """
        response = self.session.delete(self._full_path(remote_path))
        return response.status_code in (200, 204)

    def exists(self, remote_path: str, root_path: str = None) -> bool:
        """Check if a file or directory exists.

        Makes a HEAD request to check if the path exists on SWITCHdrive.

        Args:
            remote_path: Path to check
            root_path: Optional override for instance root_path

        Returns:
            True if path exists, False otherwise
        """
        response = self.session.head(self._full_path(remote_path, root_path))
        return response.status_code == 200

    file_exists = exists # alias

    def read_text(self, remote_path: str) -> str:
        """Read a text file's contents.

        Downloads and returns the content of a text file from SWITCHdrive.

        Args:
            remote_path: Path of text file to read

        Returns:
            File contents as string

        Raises:
            FileNotFoundError: If file does not exist
        """
        response = self.session.get(self._full_path(remote_path))
        if response.status_code == 200:
            return response.text
        raise FileNotFoundError(f"File not found: {remote_path}")

    def write_text(self, remote_path: str, content: str) -> bool:
        """Write text content to a file.

        Creates necessary directories and uploads text content to SWITCHdrive.

        Args:
            remote_path: Destination file path
            content: Text content to write

        Returns:
            True if write succeeded, False otherwise
        """
        full_path = self._full_path(remote_path)
        self.ensure_folder_exists(full_path)
        response = self.session.put(full_path, data=content.encode('utf-8'))
        return response.status_code in (200, 201, 204)

    def list_files(self, remote_path: str) -> list:
        """List files in a directory.

        Makes a PROPFIND request to get directory contents from SWITCHdrive.

        Args:
            remote_path: Directory path to list

        Returns:
            List of filenames in the directory, empty list on error
        """
        try:
            full_remote_path = self._full_path(remote_path)
            response = self.session.request('PROPFIND', full_remote_path, headers={'Depth': '1'})
            
            if not response.ok:
                print(f"Error listing files: {response.status_code} {response.text}")
                return []
            
            # Parse the response to extract file names
            # This is a simplified example; you may need to adjust based on the actual response format
            from xml.etree import ElementTree as ET
            tree = ET.fromstring(response.content)
            files = []
            for response in tree.findall('{DAV:}response'):
                href = response.find('{DAV:}href').text
                filename = os.path.basename(href)
                if filename:  # Exclude directories
                    files.append(filename)
            
            print(f"Files in {remote_path}: {files}")  # Debug output
            return files
        except Exception as e:
            print(f"Error listing files: {e}")
            return []