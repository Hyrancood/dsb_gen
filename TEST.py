import json, sys, copy


# facing = {'south': 'west', 'west': 'north', 'north': 'east', 'east': 'south'}
facing = {'south': 'east', 'east': 'north', 'north': 'west', 'west': 'south'}

def rotate90_element(predicate):
  global facing
  result = {"condition": predicate['condition'],}
  x, y, z = predicate.get('offsetZ', 0), predicate.get('offsetY', 0), -predicate.get('offsetX', 0)
  if x != 0:
    result['offsetX'] = x
  if y != 0:
    result['offsetY'] = y
  if z != 0:
    result['offsetZ'] = z
  result['predicate'] = copy.deepcopy(predicate['predicate'])
  if 'block' in predicate['predicate']:
    if 'state' in predicate['predicate']['block']:
      if 'facing' in predicate['predicate']['block']['state']:
        print("!")
        new_facing = facing[result['predicate']['block']['state']['facing']]
        print(result['predicate']['block']['state']['facing'], new_facing)
        result['predicate']['block']['state']['facing'] = str(new_facing)
        print(f"p: {predicate['predicate']['block']}\nr: {result['predicate']['block']}")
  return result


def rotate90_list(predicate_list: list):
  result = []
  for element in predicate_list:
    result.append(rotate90_element(element))
  return result


def rotate_90_terms(predicate):
  return {'condition': predicate['condition'], 'terms': rotate90_list(predicate['terms'])}


args = sys.argv
path = args[1]
output = args[2]
func = rotate90_list
if len(args) >= 4 and args[3] == '-t':
  func = rotate_90_terms
with open(path) as file:
  jsoncontent = ''.join(file.readlines()).strip().replace("\n", "")
predicate = json.loads(jsoncontent)
print(predicate)
result = {'condition': 'minecraft:any_of', 'terms':[predicate]}
for i in range(1, 4):
  predicate = func(predicate)
  result['terms'].append(predicate)
print()
print(result)
with open(output, 'w') as file:
  file.write(json.dumps(result))
