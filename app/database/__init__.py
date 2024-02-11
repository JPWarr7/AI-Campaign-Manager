from app import mysql
from MySQLdb import cursors
from os import path
from .login import *
from .register import *
from .profile import *
from .stocks import *
from .shares import *
from .requests import *


def read_sql(filename):
    """
    Takes the name of a file and executes the corresponding SQL file
    This is intended for use with SQL queries that DO NOT depend on any application data

    Examples:
    - Creating and Dropping Tables
    - Insertion of test data

    Ensure the SQL file you are attempting to read and execute is in the queries folder
    """
    file_path = path.join(*__path__, f"queries\\{filename}.sql")
    print(f"Running commands in {file_path}")

    file = open(file_path, "r")
    sql_file = file.readlines()
    parser = SQLParser()
    commands = parser.parse_commands(sql_file)
    file.close()

    cursor = mysql.connection.cursor(cursors.DictCursor)
    for command in commands:
        cursor.execute(command)
        mysql.connection.commit()
    print(f"Executed all commands in {filename}.sql")


def is_str_token(token):
    return token == "\'" or token == "\"" or token == "`"


def is_comment_token(token):
    return token == "#" or token == "--"


class SQLParser:
    def __init__(self):
        self.commands = []  # parsed sql commands
        self.current = []  # current sql command
        self.tokens = []  # token list
        self.is_str = None  # current string token
        self.is_comment = False  # line comments
        self.block_comment = 0  # block comments

    def check_token(self, token):
        if self.is_str:  # currently open string
            if self.is_str == token:
                self.is_str = None  # close string, if possible
            return True  # anything goes inside a string
        if token == "/*":  # open block comment
            self.block_comment += 1
            return False
        if token == "*/":  # closed block comment
            self.block_comment -= 1
            return False
        if self.is_comment or self.block_comment > 0:  # within comment
            return False
        if is_comment_token(token):  # start of single line comment
            self.is_comment = True
            return False
        if is_str_token(token):
            self.is_str = token
        return True

    def parse_token(self, token):
        word = []
        for char in token:
            word.append(char)
            if not char == ";":
                continue  # inclusive split words with ";"
            self.tokens.append("".join(word))
            word = []
        if word:
            self.tokens.append("".join(word))
        return token

    def parse_line(self, line: str):
        self.tokens = []
        self.is_comment = False
        for token in line.split():  # parse line into sql tokens
            self.parse_token(token)
        for token in self.tokens:
            if not self.check_token(token):
                continue  # check token
            self.current.append(token)  # add it to command if valid

            if self.is_str:
                continue  # open string
            if not token.endswith(";"):
                continue  # Not end of command
            self.build_command()

    def build_command(self):
        command = " ".join(self.current)
        self.commands.append(command)
        self.current = []

    def parse_commands(self, file):
        for line in file:
            self.parse_line(line)
        if self.current:
            self.build_command()
        return self.commands
