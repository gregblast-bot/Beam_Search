import StringDouble
import heapq
import math


#  ​‌​​‌​​‌​‌‌​​‌‌‌​‌‌​‌‌‌​​‌‌​‌‌‌‌​‌‌‌​​‌​​‌‌​​‌​‌​​‌​​​​​​‌‌​​​​‌​‌‌​‌‌​​​‌‌​‌‌​​​​‌​​​​​​‌‌‌​​​​​‌‌‌​​‌​​‌‌​​‌​‌​‌‌‌​‌‌​​‌‌​‌​​‌​‌‌​‌‌‌‌​‌‌‌​‌​‌​‌‌‌​​‌‌​​‌​​​​​​‌‌​‌​​‌​‌‌​‌‌‌​​‌‌‌​​‌‌​‌‌‌​‌​​​‌‌‌​​‌​​‌‌‌​‌​‌​‌‌​​​‌‌​‌‌‌​‌​​​‌‌​‌​​‌​‌‌​‌‌‌‌​‌‌​‌‌‌​​‌‌‌​​‌‌​​‌​‌‌‌​​​‌​​​​​​‌​​‌‌‌​​‌‌​‌‌‌‌​‌‌‌​‌‌‌​​‌​​​​​​‌‌​​​​‌​‌‌​‌‌‌​​‌‌‌​​‌‌​‌‌‌​‌‌‌​‌‌​​‌​‌​‌‌‌​​‌​​​‌​​​​​​‌‌‌​​​‌​‌‌‌​‌​‌​‌‌​​‌​‌​‌‌‌​​‌‌​‌‌‌​‌​​​‌‌​‌​​‌​‌‌​‌‌‌‌​‌‌​‌‌‌​​‌‌‌​​‌‌​​‌​​​​​​‌‌​​​​‌​‌‌​‌‌‌​​‌‌​​‌​​​​‌​​​​​​‌‌‌​​​​​‌‌‌​​‌​​‌‌​‌‌‌‌​‌‌‌​‌‌​​‌‌​‌​​‌​‌‌​​‌​​​‌‌​​‌​‌​​‌​​​​​​‌‌​​‌‌‌​‌‌‌​‌​‌​‌‌​‌​​‌​‌‌​​‌​​​‌‌​​​​‌​‌‌​‌‌‌​​‌‌​​​‌‌​‌‌​​‌​‌​​‌​​​​​​‌‌​‌​​‌​‌‌​‌‌‌​​​‌​​​​​​‌‌​​​​‌​​‌​​​​​​‌‌​​‌‌​​‌‌​​​​‌​‌‌​‌​​‌​‌‌‌​‌​​​‌‌​‌​​​​‌‌​​‌‌​​‌‌‌​‌​‌​‌‌​‌‌​​​​‌​​​​​​‌‌‌​‌‌‌​‌‌​​​​‌​‌‌‌‌​​‌​​‌​​​​​​‌‌​​​‌​​‌‌‌​‌​‌​‌‌‌​‌​​​​‌​​​​​​‌‌​​‌‌‌​‌‌​​‌​‌​‌‌​‌‌‌​​‌‌​​‌​‌​‌‌‌​​‌​​‌‌​​​​‌​‌‌‌​‌​​​‌‌​​‌​‌​​‌​​​​​​‌‌‌​‌‌‌​‌‌‌​​‌​​‌‌​‌‌‌‌​‌‌​‌‌‌​​‌‌​​‌‌‌​​‌​​​​​​‌‌​​​‌‌​‌‌​‌‌‌‌​‌‌​​‌​​​‌‌​​‌​‌​‌‌‌​​‌‌​​‌​‌‌‌​BeamSearch Class
class BeamSearch:

    graph = []

    def __init__(self, input_graph):
        self.graph = input_graph
        return

    def beamSearchV1(self, pre_words, beamK, maxToken):
            # Basic beam search.
            sentence = ""
            probability = 1.0
            score = 0.0
            tokens = pre_words.split()
            
            # Calculate the starting score of the pre_words
            for i in range(len(tokens) - 1):
                head_word = tokens[i]
                tail_word = tokens[i + 1]
                prob = self.graph.getProb(head_word, tail_word)
                if prob > 0:
                    # Since these probabilities are conditional and we are using the log operation, add the current and previous scores
                    probability *= prob
                    score += math.log(prob)

            # Store the pre_words and its calculated score as the initial sentence
            sentences = [[tokens, score, probability]]

            # True until we hit max token limit or have a complete sentence
            while True:
                possible_sentences = []
                can_expand = False
                
                for tokens, score, probability in sentences:
                    head_word = tokens[-1] # The new head_word is the last token in the current sentence

                    # Leave loop if the token length is greater than or equal to the max token limit and if head_word is the end of sentence token
                    # Otherwise, get all possible next words
                    if len(tokens) >= maxToken or head_word == '</s>':
                        possible_sentences.append([tokens, score, probability])
                        continue
                    else:
                        tails = self.graph.getTails(head_word)

                    # If we have possible next words, expand each path and calculate new scores. Otherwise, we've reached a dead end
                    if tails:
                        can_expand = True
                        for tail_word in tails:
                            prob = self.graph.getProb(head_word, tail_word)
                            if prob > 0:
                                new_probability = probability * prob
                                new_score = score + math.log(prob)
                                possible_sentences.append([tokens + [tail_word], new_score, new_probability])
                    else:
                        possible_sentences.append([tokens, score, probability])
                # If no paths were able to add a new word, we are done
                if not can_expand:
                    break

                # Prune depending on beam width. Sort by probability, where the negative value closest to zero is the highest probability, and keep top k
                # ordered = sorted(possible_sentences, key=lambda x: x[1], reverse=True)
                # sentences = ordered[:beamK]

                # Prune depending on beam width. Use nlargest (O(N log K) complexity) instead of full sort (O(N log N) complexity)
                sentences = heapq.nlargest(beamK, possible_sentences, key=lambda x: x[1])

            # The best sentence is the first in the list after sorting. Recreate the sentence string from the tokens.
            best_tokens, best_score, best_probability = sentences[0] 
            sentence = " ".join(best_tokens)
            print(f"*"*50)
            print(f"Best probability: {best_probability}")
            
            return StringDouble.StringDouble(sentence, best_score)

    def beamSearchV2(self, pre_words, beamK, param_lambda, maxToken):
    	# Beam search with sentence length normalization.
        sentence = ""
        probability = 0.0
        return StringDouble.StringDouble(sentence, probability)
