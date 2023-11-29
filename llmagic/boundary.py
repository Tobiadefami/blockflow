from llmagic.dtypes import Boundary, TruncationStrategy


class SpacyPlugin:
    def __init__(self):
        self.nlp = None

    @property
    def sentence_splitter(self):
        import spacy

        if self.nlp is None:
            self.nlp = spacy.blank("en")
            self.nlp.add_pipe("sentencizer")
        return self.nlp


SPACY_MODEL = SpacyPlugin()


@profile
def find_boundary_points(
    encoding, tokenizer, boundary: Boundary, truncate: TruncationStrategy
) -> list[int]:
    """
    Return token indices that correspond to valid boundary points
    """
    boundary_points: list[int] = []
    if boundary == "token":
        return list(range(len(encoding.ids)))
    elif boundary == "line":
        boundary_token = tokenizer.encode("\n").ids[0]
        boundary_points.extend(
            [i for i, token in enumerate(encoding.ids) if token == boundary_token]
        )
    elif boundary == "whitespace":
        whitespace_token = "Ġ"
        boundary_points.extend(
            [
                i
                for i, token in enumerate(encoding.tokens)
                if token.startswith(whitespace_token)
            ]
        )

    # elif boundary == "sentence":
    #     decoded_text = tokenizer.decode(encoding.ids)
    #     doc = SPACY_MODEL.sentence_splitter(decoded_text)

    #     search_start_idx = 0
    #     for sent_idx, sentence in enumerate(doc.sents):
    #         for offset_idx, (token_char_start, token_char_end) in enumerate(
    #             encoding.offsets[search_start_idx:]
    #         ):
    #             token_idx = search_start_idx + offset_idx
    #             if truncate == "right":
    #                 if token_char_start <= sentence.start_char <= token_char_end:
    #                     boundary_points.append(token_idx)
    #                     search_start_idx = token_idx
    #                     break
    #             elif truncate == "left":
    #                 if token_char_start <= sentence.end_char <= token_char_end:
    #                     boundary_points.append(token_idx)
    #                     search_start_idx = token_idx
    #                     break

    elif boundary == "sentence":
        decoded_text = tokenizer.decode(encoding.ids)
        doc = SPACY_MODEL.sentence_splitter(decoded_text)

        # preprocess the sentence
        sentence_boundaries = [(sent.start_char, sent.end_char) for sent in doc.sents]

        start_idx = 0
        for offset_idx, (token_start, token_end) in enumerate(encoding.offsets):
            # exit early if all sentences have been processed
            if start_idx >= len(sentence_boundaries):
                break  # already processed

            char_start, char_end = sentence_boundaries[start_idx]

            if truncate == "right" and token_start <= char_start <= token_end:
                boundary_points.append(offset_idx)
                start_idx += 1

            if truncate == "left" and token_start <= char_end <= token_end:
                boundary_points.append(offset_idx)
                start_idx += 1

    else:
        raise NotImplementedError(f"Boundary {boundary} not implemented")
    return boundary_points
