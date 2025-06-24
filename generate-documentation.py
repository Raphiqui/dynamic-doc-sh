    """
    Point is to check that the target file specified (the `.sh` script)
    has somehow changed using the hash of the file.

    If it did then perform the creation of a new one. Just delete if exists
    already or create. Then, read it and create the prompts lines. Then use the template
    from jinja2 to generate the documentation.
    """
        """
        Check that the current sequence has the correct values or at least the one required 
        if not just erase it due to some and print a log
        """
        """
        Simple file reader to read the .sh file and
        possibly parse it or gather the reading inputs found

        Let's assume we have some decorators in the same model of swagger
        So, there is a #question decorator, which is for now a comment but whatever
        in the .sh file, whatever comes after must be
        processed as the question until reaching ...
        """

"""
    def _get_hash(self) -> hashlib.sha256:

        try:
            os.path.exists(path)
        except Exception as e:
            print(e)

        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()


        print(os.path.exists("test.sh"))
        print(hash_file_content("test.sh"))
"""

