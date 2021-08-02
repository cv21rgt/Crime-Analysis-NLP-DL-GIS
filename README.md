# Introduction

Crime analysis is not only an essential part of efficient law enforcement for any city or country, it also informs citizens on how safe their neighbourhoods are - which in turn helps them to make informed decisions such as where they would like to live or work in the long term. In order to start the analysis, first and foremost we need analyzable data. This is not usually a problem for developed countries, all you have to do is "Google" crime statistics and the data is made available to you in table, interactive maps or other forms. However, it's not so simple for less developed countries. In most cases the data is not collected at all due to scarce resources and priorities lie elsewhere. In cases where the data is available, it is surrounded by bureaucratic red tape which makes data access impossible. In some cases you have to pay to access such data, which governments should be making available freely to their citizens.

This repository intends to extract analyzable crime data for Zimbabwe. Despite a huge volume of data being present in witness statements and police reports, it is not made available to the public. However, there is another good source of crime data - newspaper articles. Whichever local paper you read there are always detailed articles about crime. The other good thing about newspaper articles on crime is that the reporting is based on court proceedings and as such the details can be relied upon. From these articles we can extract the following information:

* Location of crime
* Date of crime
* Type of crime
* Weapon/s used if any
* Age, Gender/Sex of offender/victim

From this data this repo aims to achieve the following:

1. Use Natural Language Processing (NLP) and Deep Learning to develop an automated workflow to extract information from newspaper crime articles.
2. Use a Geographical Information System (GIS) to maintain the data and display it.

## Tools to use