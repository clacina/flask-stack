from apiflask import Schema
from apiflask.fields import Integer, String, List, Nested
from pkg_resources import require


class LoadSchema(Schema):
    source = String(metadata={'title': 'Source Folder', 'description': 'Folder to load.'})
    fileentry = String(metadata={'title': 'File Source', 'description': 'Single file to load.'})
    notes = String(metadata={'title': 'Notes', 'description': 'Optional notes for this batch.'})


class ProcessSchema(Schema):
    batch_id = Integer()
    notes = String()


class ProcessListSchema(Schema):
    files = List(Integer())
    notes = String()


"""
New Table Schema - 11/02/2024

=========================== Raw data import

UC = Unique Constraint

transaction_batch goes away

class TransactionFile:  # was transaction_batch_contents -> transaction_files
    #  Everytime we load a file, we create a new entry here
    def __init__(self):
        self.id = None      # identity
        self.filename = None                            UC
        self.institution_id = None                      UC
        self.added_date = None
        self.file_date = None                           UC
        self.notes = None
        self.transaction_count = None                   UC
        
class TransactionRecords:  # -> points to all records for ^^
    def __init__(self):
        self.id = identity
        self.batch_id = TansactionFile.id

class TransactionNotes:  # was transaction_notes
    def __init__(self):
        self.id = Identity
        self.transaction_id = linke to transaction records
        self.note = text        
        
        ----------------------------------------------------------------        
=========================== Process Raw data into category matches

class ProcessedTransactionBatch
    def __init__(self):
        self.id = Identity
        self.TransactionFile -> link to TransactionFile.id
        self.run_date - date and time processed
        self.notes
        
        
class ProcessedTransactionRecords
    def __init__(self):
        self.id = Identity
        self.batch_id = ProcessedTransactionBatch.id
                
"""
