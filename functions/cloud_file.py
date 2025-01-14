import json, yaml
import pandas as pd
from io import StringIO

class CloudFile:
    def __init__(self, path: str, storage):
        """
        Initialize a CloudFile object.

        :param path: The remote path to the file (relative to the root_path in CloudStorage).
        :param storage: An instance of the CloudStorage class.
        """
        if not isinstance(path, str):
            raise TypeError("path must be a string")
        if not hasattr(storage, 'file_exists') or not hasattr(storage, 'read_text') or not hasattr(storage, 'write_text'):
            raise TypeError("storage must implement file_exists, read_text and write_text methods")
            
        self.path = path
        self.storage = storage

    def _get_extension(self) -> str:
        """Get the file extension."""
        return self.path.split('.')[-1].lower() if '.' in self.path else ''

    def exists(self) -> bool:
        """Check if the file exists."""
        return self.storage.file_exists(self.path)

    def load(self):
        """
        Load and automatically detect the file's content type based on extension and content.

        :return: The file's content as string, dict (for JSON/YAML), or DataFrame (for CSV).
        :raises FileNotFoundError: If the file does not exist
        :raises ValueError: If file content cannot be parsed according to its extension
        """
        if not self.exists():
            raise FileNotFoundError(f"File {self.path} does not exist")
            
        content = self.storage.read_text(self.path)
        ext = self._get_extension()

        # Try loading as JSON/YAML for those extensions
        if ext in ['json', 'yaml', 'yml']:
            try:
                if ext == 'json':
                    return json.loads(content)
                else:
                    return yaml.safe_load(content)
            except (json.JSONDecodeError, yaml.YAMLError) as e:
                raise ValueError(f"Failed to parse {ext} content: {str(e)}")

        # Try loading as DataFrame for CSV
        if ext == 'csv':
            try:
                return pd.read_csv(StringIO(content))
            except pd.errors.EmptyDataError:
                return pd.DataFrame()
            except Exception as e:
                raise ValueError(f"Failed to parse CSV content: {str(e)}")

        # Default to text
        return content

    def save(self, content) -> bool:
        """
        Save content, automatically handling the format based on file extension and content type.

        :param content: The content to save (can be string, dict, or DataFrame)
        :raises ValueError: If content type doesn't match file extension
        :raises IOError: If write operation fails
        """
        ext = self._get_extension()

        try:
            # Handle DataFrame
            if isinstance(content, pd.DataFrame):
                if ext != 'csv':
                    raise ValueError("Can only save DataFrame to CSV files")
                text_content = content.to_csv(index=False)
                return self.storage.write_text(self.path, text_content)

            # Handle dict/list for JSON/YAML
            if isinstance(content, (dict, list)):
                if ext == 'json':
                    text_content = json.dumps(content)
                elif ext in ['yaml', 'yml']:
                    text_content = yaml.dump(content)
                else:
                    raise ValueError("Can only save dict/list to JSON or YAML files")
                return self.storage.write_text(self.path, text_content)

            # Handle string content
            if isinstance(content, str):
                return self.storage.write_text(self.path, content)

            raise ValueError(f"Unsupported content type: {type(content)}")

        except Exception as e:
            print(f"Error saving content: {e}")
            return False

    def delete(self) -> bool:
        """
        Delete the file.
        
        :raises IOError: If deletion fails
        """
        return self.storage.delete_file(self.path)