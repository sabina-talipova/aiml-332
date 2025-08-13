## Instructions on how to run your program on lab computers

## A list of steps you have completed

### Main actions performed at each step of the verification work: 

#### Data Preparation: 

- Training, validation, and test datasets were created to ensure proper model evaluation and to prevent overfitting. 

- Methods for preprocessing text data before feeding it into the model were developed, including: 

- Text cleaning: removal of special characters and punctuation, converting all text to lowercase for consistency. 

- Stop-word removal, eliminating common but non-informative words based on the task requirements. 

- Lemmatization or stemming to reduce words to their base or root forms, improving analysis quality. 

- Data augmentation techniques such as synonym replacement, back-translation, and others were applied when data volume was limited. 

#### Step 1: 

- A basic text classifier was created using CountVectorizer() for text representation, which converts text into frequency-based word vectors. 

- Three training algorithms were applied: KNeighborsClassifier (k-nearest neighbors), MultinomialNB (multinomial Naive Bayes), and LinearSVC (linear Support Vector Machine). 

- Performance analysis was conducted using classification_report, which provided metrics including accuracy for each algorithm. 

#### Step 2: 

- A text classifier was built using TfidfVectorizer() for text representation, which takes into account both word frequency and its importance in the corpus. 

- The same three algorithms—KNeighborsClassifier, MultinomialNB, and LinearSVC—were used for training. 

- No additional text preprocessing steps were applied in this stage. 

- Model performance was evaluated with classification_report, reporting accuracy scores for each algorithm. 

#### Step 3: 

- A text classifier based on a Convolutional Neural Network (CNN) was implemented, allowing the model to extract more complex features from text data via deep learning. 

- A graph was plotted to show how the accuracy changed during training for both the training and test datasets, helping to assess learning quality and detect overfitting. 

#### Step 4: 

- An improved version of the CNN-based classifier was developed using pretrained word embeddings from GloVe as input features. 

- A confusion matrix was constructed for this model, providing detailed insight into which classes were commonly misclassified and enabling a more nuanced evaluation beyond simple accuracy. 

#### Step 5: 

- An enhanced version of the classifier was created with several improvements: 

- More advanced data preprocessing techniques were implemented. 

- Hyperparameter tuning was performed to optimize model performance. 

- The network architecture was modified to incorporate Transformer mechanisms, improving contextual understanding. 

- Text representation was switched to BERT-based embeddings, which better capture semantic relationships between words. 

## Details of the improvements made in Step 5
#### 1. More Advanced Data Preprocessing 

- The text preprocessing pipeline was expanded and refined to improve input data quality and ensure consistency before feeding it into the model: 

- Text cleaning: Removal of unnecessary characters, such as punctuation marks, special symbols, and extra spaces. 

- Lowercasing: Converting all text to lowercase to avoid treating words with different cases as distinct tokens. 

- Lemmatization & word normalization: Reducing words to their base or dictionary form (e.g., running → run, better → good) to unify different morphological variations. 

- Data augmentation: Introducing variability into the dataset to improve model robustness, including replacing certain words with synonyms and applying back-translation when applicable. 

- Tokenization: Splitting sentences into individual tokens (words or subwords) and converting them into numerical indices suitable for embedding layers or pretrained models. 

#### 2. Model Architecture Enhancements 

- The CNN architecture used in previous steps was modified to integrate a Transformer-based architecture, enabling better capture of long-range dependencies and contextual meaning within the text. 

#### 3. Improved Text Representations 

- Replaced basic vectorizers (Count/Tf-idf) with an encoder–decoder BERT model, providing rich, context-aware word and sentence representations for better understanding of text meaning. 

## A summary of the comparison results from Step 6 with a brief analysis

