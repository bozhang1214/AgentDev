def add(a, b):
    return a + b


print(add(3, 7))

skills = ["HTML", "CSS", "JS"]
for skill in skills:
    print(f"skill: {skill}")

numbers = [1, 2, 3]
numbers.append(4)
print(f"numbers: {numbers}")
last = numbers.pop()
print(f"last of numbers: {last}\nnumbers: {numbers}")

person = {
    "name": "ZhangSan",
    "age": 25
}
print(f'person name: {person["name"]}')
