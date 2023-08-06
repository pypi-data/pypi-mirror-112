from matplotlib import pyplot as plt
import math
from keras.callbacks import LambdaCallback, EarlyStopping, ModelCheckpoint
import keras.backend as K
import numpy as np
import pandas as pd 
from keras.callbacks import LambdaCallback
import altair as alt
class sanity_check:
    
  history = None
  def __init__(self,model,start_lr=0.0001,end_lr = 1, lr_change= 10):
        
        
      self.model=model
      self.start_lr = start_lr
      self.end_lr= end_lr
      self.lr_change = lr_change

      self.cur_model  = model
      self.cur_rate = 0
      self.df = pd.DataFrame()
      model_dict = {}
      loss_record = {}
      lr_list  = []
      t= start_lr
      while t< end_lr:
            
        loss_record[str(t)] = []
        t *= lr_change

        
            
            
      self.loss_record = loss_record
      
  def check_sanity(self,train_generator,test_generator,epochs,save_weight_dir,spe = 0):
    if spe == 0:
      steps_per_epochs = len(train_generator)
    else:
      steps_per_epochs = spe
    
    for x in self.loss_record.keys():
      #K.clear_session()
      print('learning_Rate : ',x)
      self.cur_rate = float(x)
      
      #mod = models.clone_model(self.model)
      
    
      K.set_value(self.model.optimizer.lr, x)

      batchcallback = LambdaCallback(on_batch_end=lambda batch,
                                                      logs: self.on_batch_end(batch, logs))
      trainingcallback = LambdaCallback(on_train_end=lambda 
                                                      logs: self.on_train_end(logs))
      save_weights   = save_weight_dir + str(x)
      modelCheckpoint = ModelCheckpoint(save_weights,
                                  monitor = 'val_loss',
                                  save_best_only = True,
                                  mode = 'min',
                                  verbose = 2,
                                  save_weights_only = True)

      self.history = self.model.fit_generator(generator= train_generator,epochs  = epochs,steps_per_epoch =steps_per_epochs,callbacks = [modelCheckpoint],validation_data=test_generator,
    verbose = 2)
      
      #print(self.history.history['val_loss'])
      epoch_list = [i for i in range(epochs)]
      learn_list = [x for i in range(epochs)]
      lr_df = pd.DataFrame({'epochs':epoch_list,'lr_rate':learn_list,'val_loss':list(self.history.history['val_loss'])})
      self.df = pd.concat([self.df,lr_df])
      self.loss_record[x] = self.history.history['val_loss']
      

  def on_train_end(self,logs):
    
    print(self.history.history['val_loss'])
    K.clear_session()
    

  def on_batch_end(self,batch,logs):
    lr = K.get_value(self.model.optimizer.lr)
    print(logs)
    self.loss_record[self.cur_rate] += [logs['val_loss']]
  def plot_loss(self):
    table = self.df


    chart = alt.Chart(table).mark_line().encode(
    x='epochs',
    y='val_loss',
    color='lr_rate',
)
    return chart

