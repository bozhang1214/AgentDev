let mySkills = ["HTML", "CSS", "Python"];

console.log("--- My Skill List ---");
for (let i = 0; i < mySkills.length; i++) {
    console.log(mySkills[i]);
}

console.log("--- while-loop ---");
let j = 0;
while (j < mySkills.length) {
    console.log(mySkills[j]);
    j++;
}

function sum(a, b) {
    return a + b;
}

let total = sum(10, 35);
console.log("10 + 35 = ", total);

console.log("--- foreach-loop ---")
mySkills.forEach(skill => console.log(skill));

let starredSkills = mySkills.map(skill => skill + " ⭐");
console.log("加星标的技能:", starredSkills);