# Author: Robert Guthrie

import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import sys, getopt, re, nltk, timeit, random
torch.manual_seed(1)
random.seed(6)
RRule = random.random()
######################################################################
'''
word_to_ix = {"hello": 0, "world": 1}
embeds = nn.Embedding(2, 5)  # 2 words in vocab, 5 dimensional embeddings
lookup_tensor = torch.LongTensor([word_to_ix["world"]])
hello_embed = embeds(autograd.Variable(lookup_tensor))
print(hello_embed)

'''
######################################################################
# An Example: N-Gram Language Modeling
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Recall that in an n-gram language model, given a sequence of words
# :math:`w`, we want to compute
#
# .. math::  P(w_i | w_{i-1}, w_{i-2}, \dots, w_{i-n+1} )
#
# Where :math:`w_i` is the ith word of the sequence.
#
# In this example, we will compute the loss function on some training
# examples and update the parameters with backpropagation.
#

CONTEXT_SIZE = 2
EMBEDDING_DIM = 10
# We will use Shakespeare Sonnet 2
test_sentence = """START_OF_SENTENCE The mathematician ran . 
START_OF_SENTENCE The mathematician ran to the store . 
START_OF_SENTENCE The physicist ran to the store . 
START_OF_SENTENCE The philosopher thought about it . 
START_OF_SENTENCE The mathematician solved the open problem . """.split()
# The mathematician ran to the store . The physicist ran to the store . The philosopher thought about it . The mathematician solved the open problem .
# we should tokenize the input, but we will ignore that for now
# build a list of tuples.  Each tuple is ([ word_i-2, word_i-1 ], target word)
trigrams = [([test_sentence[i], test_sentence[i + 1]], test_sentence[i + 2])
            for i in range(len(test_sentence) - 2)]
# print the first 3, just so you can see what they look like
#print(trigrams)

vocab = set(test_sentence)
# this is the sequence of word.
word_to_ix = {word: i for i, word in enumerate(vocab)}
print("This is the check List",word_to_ix)


class NGramLanguageModeler(nn.Module):

    def __init__(self, vocab_size, embedding_dim, context_size):
        super(NGramLanguageModeler, self).__init__()
        self.embeddings = nn.Embedding(vocab_size, embedding_dim)
        self.linear1 = nn.Linear(context_size * embedding_dim, 128)
        self.linear2 = nn.Linear(128, vocab_size)

    def forward(self, inputs):
        embeds = self.embeddings(inputs).view((1, -1))
        out = F.relu(self.linear1(embeds))
        out = self.linear2(out)
        log_probs = F.log_softmax(out, dim=1)
        return log_probs


losses = []
loss_function = nn.NLLLoss()
model = NGramLanguageModeler(len(vocab), EMBEDDING_DIM, CONTEXT_SIZE)
# 用初始化的纬度和内容数量建立 model
optimizer = optim.SGD(model.parameters(), lr=0.1)

for epoch in range(10):
    total_loss = torch.Tensor([0])
    random.shuffle(trigrams, lambda: RRule)
    for context, target in trigrams:

        # Step 1. Prepare the inputs to be passed to the model (i.e, turn the words
        # into integer indices and wrap them in variables)
        context_idxs = [word_to_ix[w] for w in context]  # word index
        context_var = autograd.Variable(torch.LongTensor(context_idxs))
        # Step 2. Recall that torch *accumulates* gradients. Before passing in a
        # new instance, you need to zero out the gradients from the old
        # instance
        model.zero_grad()

        # Step 3. Run the forward pass, getting log probabilities over next
        # words
        log_probs = model(context_var)

        # Step 4. Compute your loss function. (Again, Torch wants the target
        # word wrapped in a variable)
        loss = loss_function(log_probs, autograd.Variable(
            torch.LongTensor([word_to_ix[target]])))
        #print(target, '+++++oooooooo')

        # Step 5. Do the backward pass and update the gradient
        loss.backward()
        optimizer.step()

        total_loss += loss.data
    losses.append(total_loss)
#print(losses)  # The loss decreased every iteration over the training data!

# The mathematician ran to the store .

check_sentence = """START_OF_SENTENCE The mathematician ran to the store . """.split()
check_trigrams = [([check_sentence[i], check_sentence[i + 1]], check_sentence[i + 2])
                  for i in range(len(check_sentence) - 2)]

check_vocab = set(check_sentence)
check_word_to_ix = {word: i for i, word in enumerate(check_vocab)}

# check_context_idxs = [word_to_ix['The'],word_to_ix['mathematician']]  # word index
# check_context_var = autograd.Variable(torch.LongTensor(check_context_idxs))
# print(model(check_context_var))
# print(word_to_ix)
# print('=================================')
# print(check_trigrams)

check_context_idxs = [word_to_ix['START_OF_SENTENCE'],word_to_ix['The']]  # word index
check_context_var = autograd.Variable(torch.LongTensor(check_context_idxs))
print(model(check_context_var))
print(word_to_ix)
print('=================================')
print(check_trigrams)

for context, target in check_trigrams:
    print('=================================')
    print('context is',context)
    check_context_idxs = [word_to_ix[w] for w in context]  # word index
    check_context_var = autograd.Variable(torch.LongTensor(check_context_idxs))
    print('----------------------------')
    print('target is', target)
    print('----------------------------')
    log_probs = model(check_context_var)
    print(log_probs)
    # sortedList, indices = torch.sort(log_probs)
    # print(sortedList)
    # print(indices)
    # print(word_to_ix[torch.max(indices)],'[][][][][]')
    print(word_to_ix)
    print('=================================')


print('NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN')
print('EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')
mathematician_var = autograd.Variable(torch.LongTensor([word_to_ix['mathematician']]))
mathematician = model.embeddings(mathematician_var)


checkList = ['physicist','philosopher']
checkVar = [autograd.Variable(torch.LongTensor([word_to_ix[item]])) for item in checkList]

# physicist_var = autograd.Variable(torch.LongTensor([word_to_ix['physicist']]))
# physicist_embedding = model.embeddings(physicist_var)

# philosopher_var = autograd.Variable(torch.LongTensor([word_to_ix['philosopher']]))
# philosopher_embedding = model.embeddings(philosopher_var)

similarityList = [torch.nn.functional.cosine_similarity(mathematician,model.embeddings(item)) for item in checkVar]

print('The result is:')
# similarity_with_physicist = torch.nn.functional.cosine_similarity(mathematician_embedding,physicist_embedding)
# similarity_with_philosopher = torch.nn.functional.cosine_similarity(mathematician_embedding,philosopher_embedding)
print('The similarity of "physicist" and "mathematician" is :',similarityList[0])
print('The similarity of "philosopher" and "mathematician" is :',similarityList[1])
print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
print('TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT')
print('=================================')



CONTEXT_SIZE = 2  # 2 words to the left, 2 to the right
'''raw_text = """We are about to study the idea of a computational process.
Computational processes are abstract beings that inhabit computers.
As they evolve, processes manipulate other abstract things called data.
The evolution of a process is directed by a pattern of rules
called a program. People create programs to direct processes. In effect,
we conjure the spirits of the computer with our spells.""".split()
'''
raw_text = """The mathematician ran .

The mathematician ran to the store .

The physicist ran to the store .

The philosopher thought about it .

The mathematician solved the open problem .""".split()
# By deriving a set from `raw_text`, we deduplicate the array
vocab = set(raw_text)
vocab_size = len(vocab)

word_to_ix = {word: i for i, word in enumerate(vocab)}
data = []
for i in range(2, len(raw_text) - 2):
    context = [raw_text[i - 2], raw_text[i - 1],
               raw_text[i + 1], raw_text[i + 2]]
    target = raw_text[i]
    data.append((context, target))
print(data[:5])


class CBOW(nn.Module):

    def __init__(self, vocab_size, embedding_dim):
        super(CBOW,self).__init__() 
        self.embeddings = nn.Embedding(vocab_size,embedding_dim)
        self.linear = nn.Linear(embedding_dim, vocab_size)

    def forward(self, inputs):
        embeds = self.embeddings(inputs)
        sum_embedding = torch.sum(embeds, dim=0).view(1,-1)
        Linear3 = self.linear(sum_embedding)
        log_probs = F.log_softmax(Linear3, dim=1)
        return log_probs


# create your model and train.  here are some functions to help you make
# the data ready for use by your module


def make_context_vector(context, word_to_ix):
    idxs = [word_to_ix[w] for w in context]
    return torch.LongTensor(idxs)


losses1 = []
loss_function = nn.NLLLoss()
model = CBOW(len(vocab), EMBEDDING_DIM)
# 用初始化的纬度和内容数量建立 model
optimizer = optim.SGD(model.parameters(), lr=0.1)

for epoch in range(10):
    total_loss = torch.Tensor([0])
    random.shuffle(trigrams, lambda: RRule)
    for context, target in data:

        # Step 1. Prepare the inputs to be passed to the model (i.e, turn the words
        # into integer indices and wrap them in variables)
        context_idxs = [word_to_ix[w] for w in context]  # word index
        context_var = autograd.Variable(torch.LongTensor(context_idxs))
        # Step 2. Recall that torch *accumulates* gradients. Before passing in a
        # new instance, you need to zero out the gradients from the old
        # instance
        model.zero_grad()

        # Step 3. Run the forward pass, getting log probabilities over next
        # words
        log_probs = model(context_var)

        # Step 4. Compute your loss function. (Again, Torch wants the target
        # word wrapped in a variable)
        loss = loss_function(log_probs, autograd.Variable(
            torch.LongTensor([word_to_ix[target]])))
        #print(target, '+++++oooooooo')

        # Step 5. Do the backward pass and update the gradient
        loss.backward()
        optimizer.step()

        total_loss += loss.data
    losses.append(total_loss)

make_context_vector(data[0][0], word_to_ix)  # example


mathematician_var = autograd.Variable(torch.LongTensor([word_to_ix['mathematician']]))
mathematician = model.embeddings(mathematician_var)


checkList = ['physicist','philosopher']
checkVar = [autograd.Variable(torch.LongTensor([word_to_ix[item]])) for item in checkList]

# physicist_var = autograd.Variable(torch.LongTensor([word_to_ix['physicist']]))
# physicist_embedding = model.embeddings(physicist_var)

# philosopher_var = autograd.Variable(torch.LongTensor([word_to_ix['philosopher']]))
# philosopher_embedding = model.embeddings(philosopher_var)

similarityList = [torch.nn.functional.cosine_similarity(mathematician,model.embeddings(item)) for item in checkVar]

print('The result is:')
# similarity_with_physicist = torch.nn.functional.cosine_similarity(mathematician_embedding,physicist_embedding)
# similarity_with_philosopher = torch.nn.functional.cosine_similarity(mathematician_embedding,philosopher_embedding)
print('The similarity of "physicist" and "mathematician" is :',similarityList[0])
print('The similarity of "philosopher" and "mathematician" is :',similarityList[1])
