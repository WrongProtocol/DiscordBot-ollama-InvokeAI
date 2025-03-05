# Carmine Silano
# Mar 5, 2025
def chunk_message(text, limit=1990):
    """
    Splits the text into chunks of at most `limit` characters.
    If a chunk ends in the middle of a code block (i.e. the number of
    triple backticks is odd), this function appends a closing code fence
    ("\n```") to that chunk and ensures that the next chunk begins with an opening
    code fence ("```\n").
    """
    chunks = []
    current_index = 0
    # This flag indicates if we are in the middle of a code block from the previous chunk.
    in_code = False
    while current_index < len(text):
        # Grab the next segment of text
        chunk_text = text[current_index : current_index + limit]
        
        # If we were already inside a code block, prepend an opening code fence.
        if in_code:
            chunk = "```\n" + chunk_text
        else:
            chunk = chunk_text

        # Calculate the total number of triple backticks:
        #   - If we're already in a code block, count that opening fence as one.
        #   - Then count the occurrences in the current chunk_text.
        code_fence_count = (1 if in_code else 0) + chunk_text.count("```")

        # If the overall count is odd, then this chunk ends with an unclosed code block.
        # Close it with a closing fence and mark that the next chunk should resume code formatting.
        if code_fence_count % 2 == 1:
            chunk += "\n```"
            in_code = True
        else:
            in_code = False

        chunks.append(chunk)
        current_index += limit

    return chunks