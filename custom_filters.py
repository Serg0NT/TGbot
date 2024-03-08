anonymous_filter = lambda x: x.lower().count('я') >= 23

print(anonymous_filter('яяяяяяяяяяяяяяяяяяяяяяяя, яяяяяяяяяяяяяяяя и яяяяяяяя тоже!'))

# x = 'яяяяяяяяяяяяяяяяяяяяЯЯяя, яяяяяяяяяяяяяяяя и яяяяяяяя тоже!'
# c = [i for i in x.split() if i.lower()=='я']
# print(c)

# print(x.lower().count('я'))