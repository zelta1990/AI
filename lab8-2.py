import csv
def posterior(prior, likelihood, observation):
    pt = 1
    pf = 1
    p1 = prior
    p2 = 1- prior
    for i in range(len(likelihood)):
        if observation[i] == True:
            p1 = p1 * likelihood[i][1]
            p2 = p2 * likelihood[i][0]
        else:
            p1 = p1 * (1-likelihood[i][1])
            p2 = p2 * (1-likelihood[i][0])
            
    pt = p1/(p1+p2)
    return pt

def learn_prior(file_name, pseudo_count=0):
    true_count = 0
    with open(file_name) as in_file:
        training_examples = [tuple(row) for row in csv.reader(in_file)]
    for i in training_examples[1:]:
        if i[12] == "1":
            true_count += 1
    prior = (pseudo_count+ true_count)/(pseudo_count+(len(training_examples)-1+pseudo_count))
    return prior

def learn_likelihood(file_name, pseudo_count=0):
    seq = []
    false_count = 0
    true_count = 0
    for i in range(12):
        seq.append([0,0])
    result = []
    with open(file_name) as in_file:
        training_examples = [tuple(row) for row in csv.reader(in_file)] 
        
    for i in range(len(training_examples)):
        if training_examples[i][12] == "0":
            false_count += 1
        else:
            true_count += 1
        for n in range(len(seq)):
            if training_examples[i][n] == "1":
                if training_examples[i][12] == "0":
                    seq[n][0] +=1                    
                elif training_examples[i][12] == "1":
                    seq[n][1] += 1
    p_spam = learn_prior(file_name, pseudo_count)
    p_nonspam = 1-p_spam
    for n in range(len(seq)):        
        pf = (seq[n][0]+pseudo_count)/(false_count+pseudo_count*2)
        pt = (seq[n][1]+pseudo_count)/(len(training_examples[1:])-false_count+pseudo_count*2)
        result.append((pf,pt))
    return result
        
    
            
def nb_classify(prior, likelihood, input_vector):
    predictions = []
    result = "Spam"
    pt = posterior(prior, likelihood, input_vector)
    if pt <= 0.5:
        result = "Not Spam"
        response = (result,1-pt)
    else:
        response = (result,pt)
             
    return response
        
def accuracy(predicted_labels, correct_labels):
    true_count = 0
    result = [(a == b) for a, b in zip(predicted_labels,correct_labels)]
    for i in result:
        if i == True:
            true_count += 1
    p_accuracy = true_count/len(result)
    return p_accuracy
    
    

#example#
'''print("Prior probability of spam is {:.5f}.".format(prior))
    
prior = learn_prior("spam-labelled.csv")
print("Prior probability of not spam is {:.5f}.".format(1 - prior))

prior = learn_prior("spam-labelled.csv", pseudo_count = 1)
print(format(prior, ".5f"))

prior = learn_prior("spam-labelled.csv", pseudo_count = 2)
print(format(prior, ".5f"))
 
prior = learn_prior("spam-labelled.csv", pseudo_count = 10)
print(format(prior, ".5f"))

prior = learn_prior("spam-labelled.csv", pseudo_count = 100)
print(format(prior, ".5f"))

prior = learn_prior("spam-labelled.csv", pseudo_count = 1000)
print(format(prior, ".5f"))'''

#example2#
'''likelihood = learn_likelihood("spam-labelled.csv")
print(len(likelihood))
print([len(item) for item in likelihood])


likelihood = learn_likelihood("spam-labelled.csv")

print("P(X1=True | Spam=False) = {:.5f}".format(likelihood[0][False]))
print("P(X1=False| Spam=False) = {:.5f}".format(1 - likelihood[0][False]))
print("P(X1=True | Spam=True ) = {:.5f}".format(likelihood[0][True]))
print("P(X1=False| Spam=True ) = {:.5f}".format(1 - likelihood[0][True]))


likelihood = learn_likelihood("spam-labelled.csv", pseudo_count=1)

print("With Laplacian smoothing:")
print("P(X1=True | Spam=False) = {:.5f}".format(likelihood[0][False]))
print("P(X1=False| Spam=False) = {:.5f}".format(1 - likelihood[0][False]))
print("P(X1=True | Spam=True ) = {:.5f}".format(likelihood[0][True]))
print("P(X1=False| Spam=True ) = {:.5f}".format(1 - likelihood[0][True]))'''


#example3#
'''prior = learn_prior("spam-labelled.csv")
likelihood = learn_likelihood("spam-labelled.csv")

input_vectors = [
    (1,1,0,0,1,1,0,0,0,0,0,0),
    (0,0,1,1,0,0,1,1,1,0,0,1),
    (1,1,1,1,1,0,1,0,0,0,1,1),
    (1,1,1,1,1,0,1,0,0,1,0,1),
    (0,1,0,0,0,0,1,0,1,0,0,0),
    ]

predictions = [nb_classify(prior, likelihood, vector) 
               for vector in input_vectors]

for label, certainty in predictions:
    print("Prediction: {}, Certainty: {:.5f}"
          .format(label, certainty))

print()   
prior = learn_prior("spam-labelled.csv", pseudo_count=1)
likelihood = learn_likelihood("spam-labelled.csv", pseudo_count=1)

input_vectors = [
    (1,1,0,0,1,1,0,0,0,0,0,0),
    (0,0,1,1,0,0,1,1,1,0,0,1),
    (1,1,1,1,1,0,1,0,0,0,1,1),
    (1,1,1,1,1,0,1,0,0,1,0,1),
    (0,1,0,0,0,0,1,0,1,0,0,0),
    ]

predictions = [nb_classify(prior, likelihood, vector) 
               for vector in input_vectors]

for label, certainty in predictions:
    print("Prediction: {}, Certainty: {:.5f}"
          .format(label, certainty))'''

#example4#
print(accuracy((True, False, True, False),
               (True, True, False, False)))

