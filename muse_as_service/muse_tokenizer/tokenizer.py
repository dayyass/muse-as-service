from typing import List

from tensorflow.core.protobuf.saved_model_pb2 import SavedModel
from tensorflow.python.saved_model.loader_impl import parse_saved_model  # noqa: F401
from tensorflow_text.python.ops.sentencepiece_tokenizer import SentencepieceTokenizer


def get_tokenizer_from_saved_model(saved_model: SavedModel) -> SentencepieceTokenizer:
    """
    Get muse_tokenizer from tf SavedModel.

    :param SavedModel saved_model: tf SavedModel.
    :return: muse_tokenizer.
    :rtype: SentencepieceTokenizer
    """

    # extract functions that contain SentencePiece somewhere in there
    functions_with_sp = [
        f
        for f in saved_model.meta_graphs[0].graph_def.library.function
        if "sentencepiecetokenizeop" in str(f).lower()
    ]

    assert len(functions_with_sp) == 1

    # find SentencePieceOp (contains the model) in the found function
    nodes_with_sp = [
        n for n in functions_with_sp[0].node_def if n.op == "SentencepieceOp"
    ]

    assert len(nodes_with_sp) == 1

    # we can pretty much save the model into a file since it does not change
    model = nodes_with_sp[0].attr["model"].s

    # instantiate the model
    tokenizer = SentencepieceTokenizer(model)

    return tokenizer


def tokenize(
    sentence: str, tokenizer: SentencepieceTokenizer, encoding: str = "utf-8"
) -> List[str]:
    """
    Tokenize sentence given muse_tokenizer.

    :param str sentence: sentence to tokenize.
    :param SentencepieceTokenizer tokenizer: muse_tokenizer.
    :param str encoding: encoding (default: "utf-8").
    :return: tokenized sentence.
    :rtype: List[str]
    """

    tokenized_sentence = []

    token_ids = tokenizer.tokenize(sentence).numpy()
    for token_id in token_ids:
        bytes_token = tokenizer.id_to_string(token_id).numpy()
        token = bytes_token.decode(encoding)
        tokenized_sentence.append(token)

    return tokenized_sentence
