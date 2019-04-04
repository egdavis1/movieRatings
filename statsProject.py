import argparse
import json
import math
import requests
import urllib

def outputMath(mean, stdDev, mathFile):
  with open(mathFile, 'a+') as file:
    file.write('Mean: ' + str(mean) + '\n')
    file.write('Std Dev: ' + str(stdDev) + '\n')

def doMath(ratings, mathFile):
  stdDev = 0
  sumNum = 0
  totalRatings = 0
  for num in ratings:
    if num != '':
      sumNum += num
      totalRatings+= 1

  mean = sumNum/float(totalRatings)

  for num in ratings:
    if num != '':
      stdDev += pow((num - mean), 2)
  if (totalRatings - 1) > 0:
    stdDev = math.sqrt(stdDev/(float(totalRatings)-1))
  else:
    stdDev = 'N/A'

  outputMath(mean, stdDev, mathFile)

def getMovieTitle(movieTitle, fileName):
  with open(fileName, 'r') as fileTitles:
    for title in fileTitles:
      title = title.strip()
      title = urllib.quote(title)
      movieTitle.append(title)
    
def printRatingsToFile(ratings, fileName):
  with open(fileName, 'w') as fileRatings:
    for rating in ratings:
      fileRatings.write(str(rating))
      fileRatings.write('\n')

def startProgram(url, apiKey, fileName, outputFile, extraFile, mathFile):
  movieTitle = []
  ratings = []
  getMovieTitle(movieTitle, fileName)

#  print(movieTitle)
  for title in movieTitle:
    apiRequest = url + '?api_key=' + apiKey + '&query=' + title

    response = requests.get(apiRequest)
    data = []
    data.append(response.json())
#    print(response)
#    print(data)
#    print(data)
#    print('')
#    print(data[0]['results'][0]['vote_average'])

    try:
      ratings.append(data[0]['results'][0]['vote_average'])
    except:
      with open(extraFile, 'a+') as file:
        file.write(urllib.unquote(title) + '\n')
      ratings.append('')

#  print(ratings)

  printRatingsToFile(ratings, outputFile)
  doMath(ratings, mathFile)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='stats project')
  parser.add_argument('-u', '--url', help = 'url for aoi call')
  parser.add_argument('-k', '--api_key', help = 'api needed for api call')
  parser.add_argument('-f', '--file_name', help = 'name of file with movie titles in it')
  parser.add_argument('-o', '--output_file', help = 'name of the output file for ratings')
  parser.add_argument('-e', '--extra_file', help = 'name of the output file that will contain movie titles that were not found in the database')
  parser.add_argument('-m', '--math_file', help = 'name of output file containing math calculations, optional. Will use outputFile (-o) instead if not entered)')
  args = parser.parse_args()

  url = args.url
  api_key = args.api_key
  file_name = args.file_name
  output_file = args.output_file
  extra_file = args.extra_file

  if args.math_file:
    math_file = args.math_file
  else:
    math_file = output_file

startProgram(url, api_key, file_name, output_file, extra_file, math_file)
