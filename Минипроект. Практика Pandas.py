#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Импортируйте библиотеку pandas как pd
import pandas as pd


# In[97]:


# Загрузите датасет bookings.csv с разделителем ;
bookings = pd.read_csv('https://stepik.org/media/attachments/lesson/360344/bookings.csv', sep=';')


# In[98]:


# Проверьте размер таблицы
bookings.shape


# In[99]:


# Проверьте типы переменных
bookings.dtypes


# In[100]:


# выведите первые 7 строк, чтобы посмотреть на данные
bookings.head(7)


# In[101]:


# Приведите названия колонок к нижнему регистру и замените пробелы на знак нижнего подчеркивания
titles = []
for i in bookings.columns:
    i = i.replace(' ', '_')
    titles.append(i.lower()) 
bookings.columns = titles
bookings.head(7)


# In[102]:


# Пользователи из каких стран совершили наибольшее число успешных бронирований? Укажите топ-5.
bookings        .query('is_canceled == 0')        .groupby('country', as_index=False)        .aggregate({'is_canceled' : 'count'})        .sort_values('is_canceled', ascending=False)        .rename(columns = {'is_canceled' : 'success_bookings'}).head()


# In[103]:


# На сколько ночей в среднем бронируют отели разных типов?
bookings        .groupby('hotel', as_index=False)        .aggregate({'stays_total_nights' : 'mean'})        .sort_values('stays_total_nights', ascending=False)        .round(decimals = 2)
        


# In[104]:


# Иногда тип номера, полученного клиентом (assigned_room_type), 
# отличается от изначально забронированного (reserved_room_type). 
# Такое может произойти, например, по причине овербукинга. Сколько подобных наблюдений встретилось в датасете?
bookings        .query('assigned_room_type != reserved_room_type')        .shape


# In[105]:


# Проанализируйте даты запланированного прибытия. 
# – На какой месяц чаще всего успешно оформляли бронь в 2016? 
bookings        .query('is_canceled == 0' and 'arrival_date_year == 2016')        .groupby('arrival_date_month', as_index=False)        .aggregate({'is_canceled' : 'count'})        .sort_values('is_canceled', ascending=False)        .rename(columns = {'is_canceled' : 'success_bookings'})        .head(1)


# In[106]:


# Изменился ли самый популярный месяц в 2017?
bookings        .query('is_canceled == 0' and 'arrival_date_year == 2017')        .groupby('arrival_date_month', as_index=False)        .aggregate({'is_canceled' : 'count'})        .sort_values('is_canceled', ascending=False)        .rename(columns = {'is_canceled' : 'success_bookings'})        .head(1)


# In[107]:


# Проанализируйте даты запланированного прибытия. 
# – Сгруппируйте данные по годам и проверьте, на какой месяц бронирования отеля типа City Hotel 
# отменялись чаще всего в каждый из периодов.
bookings        .query("is_canceled == 1" and "hotel == 'City Hotel'")        .groupby('arrival_date_year')        ['arrival_date_month'].value_counts()        
        


# In[108]:


# Посмотрите на числовые характеристики трёх колонок: adults, children и babies. Какая из них имеет наибольшее среднее значение?
bookings[['adults', 'children', 'babies']].mean()


# In[109]:


# Создайте колонку total_kids, объединив столбцы children и babies. 
# Для отелей какого типа среднее значение переменной оказалось наибольшим?
# City hotel – отель находится в городе
# Resort hotel – отель курортный
bookings['total_kids'] = bookings['children'] + bookings['babies']
bookings        .groupby('hotel', as_index=False)        .aggregate({'total_kids' : 'mean'})        .sort_values('total_kids', ascending=False)        .round(2).head(1)


# In[110]:


# Не все бронирования завершились успешно (is_canceled), поэтому можно посчитать, 
# сколько клиентов было потеряно в процессе. Churn rate (отток, коэффициент оттока) – это процент подписчиков 
# (например, на push-уведомления от сайта), которые отписались от канала коммуникации, 
# отказались от услуг сервиса в течение определенного периода времени. Иными словами, 
# представляет собой отношение количества ушедших пользователей к общему количеству пользователей, выраженное в процентах.

# Создайте переменную has_kids, которая принимает значение True, если клиент при бронировании указал хотя бы одного ребенка 
# (total_kids), в противном случае – False. Далее проверьте, среди какой группы пользователей показатель оттока выше. 
# В качестве ответа укажите наибольший %, округленный до 2 знаков после точки 
# (то есть доля 0.24563 будет 24.56% и в ответ пойдёт 24.56)

bookings['has_kids'] = bookings['total_kids'] > 0
have_kids_churn = round(bookings.query('is_canceled == 1 and has_kids == True')                                .shape[0]/bookings.query('has_kids == True').shape[0]*100, 2)
no_kids_churn = round(bookings.query('is_canceled == 1 and has_kids == False')                              .shape[0]/bookings.query('has_kids == False').shape[0]*100, 2)


# In[111]:


have_kids_churn


# In[112]:


no_kids_churn


# In[ ]:




