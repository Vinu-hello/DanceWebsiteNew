const questions = [
    { question: "Do you feel you understand your child's emotions?", options: ["Yes", "Sometimes", "Rarely", "No"], values: [4, 3, 2, 1] },
    { question: "How often do you talk with your child about their day?", options: ["Every day", "Weekly", "Monthly", "Never"], values: [4, 3, 2, 1] },
    { question: "Do you encourage your child to share their feelings?", options: ["Always", "Often", "Sometimes", "Never"], values: [4, 3, 2, 1] },
    { question: "How involved are you in your child's hobbies?", options: ["Very involved", "Somewhat", "Rarely", "Not at all"], values: [4, 3, 2, 1] },
    { question: "Do you set aside time specifically for family?", options: ["Yes, daily", "Yes, weekly", "Occasionally", "No"], values: [4, 3, 2, 1] },
    { question: "Do you listen without interrupting?", options: ["Always", "Mostly", "Sometimes", "Rarely"], values: [4, 3, 2, 1] },
    { question: "Do you encourage independence in decision-making?", options: ["Always", "Often", "Sometimes", "Never"], values: [4, 3, 2, 1] },
    { question: "How well do you handle your own stress around your child?", options: ["Very well", "Somewhat", "Not well", "Poorly"], values: [4, 3, 2, 1] },
    { question: "How do you discipline your child?", options: ["Constructively", "Sometimes calmly", "Often angrily", "Never"], values: [4, 3, 2, 1] },
    { question: "Do you know your child’s friends?", options: ["Yes, very well", "Somewhat", "Barely", "No"], values: [4, 3, 2, 1] },
    { question: "Do you help with school-related tasks?", options: ["Always", "Sometimes", "Rarely", "Never"], values: [4, 3, 2, 1] },
    { question: "Do you encourage self-confidence?", options: ["Always", "Often", "Sometimes", "Never"], values: [4, 3, 2, 1] },
    { question: "Do you model positive behavior?", options: ["Always", "Often", "Sometimes", "Rarely"], values: [4, 3, 2, 1] },
    { question: "Do you set boundaries respectfully?", options: ["Always", "Usually", "Sometimes", "Rarely"], values: [4, 3, 2, 1] },
    { question: "Do you appreciate your child’s efforts?", options: ["Always", "Often", "Sometimes", "Rarely"], values: [4, 3, 2, 1] },
];
// Questions for the child
const childQuestions = [
    { question: "Do you feel comfortable talking about your feelings?", options: ["Always", "Sometimes", "Rarely", "Never"], values: [4, 3, 2, 1] },
    { question: "Do you feel listened to by your parents?", options: ["Always", "Sometimes", "Rarely", "Never"], values: [4, 3, 2, 1] },
    { question: "How often do you feel happy?", options: ["Often", "Sometimes", "Rarely", "Never"], values: [4, 3, 2, 1] },
    { question: "Do you have a close friend?", options: ["Yes", "A few", "Not really", "No"], values: [4, 3, 2, 1] },
    { question: "Do you like going to school?", options: ["Yes", "Sometimes", "Rarely", "No"], values: [4, 3, 2, 1] },
    { question: "Do you feel supported by your parents?", options: ["Always", "Often", "Sometimes", "Never"], values: [4, 3, 2, 1] },
    { question: "Are you able to talk about worries?", options: ["Always", "Sometimes", "Rarely", "Never"], values: [4, 3, 2, 1] },
    { question: "How often do you feel stressed?", options: ["Rarely", "Sometimes", "Often", "Always"], values: [1, 2, 3, 4] },
    { question: "Do you feel appreciated?", options: ["Always", "Mostly", "Sometimes", "Rarely"], values: [4, 3, 2, 1] },
    { question: "Do you have time for hobbies?", options: ["Yes", "Sometimes", "Rarely", "No"], values: [4, 3, 2, 1] },
    { question: "Do you feel safe at home?", options: ["Always", "Mostly", "Sometimes", "Rarely"], values: [4, 3, 2, 1] },
    { question: "Do you get enough rest?", options: ["Always", "Mostly", "Sometimes", "Rarely"], values: [4, 3, 2, 1] },
    { question: "Do you feel close to your family?", options: ["Very close", "Close", "Somewhat", "Not at all"], values: [4, 3, 2, 1] },
    { question: "Do you enjoy time with friends?", options: ["Always", "Sometimes", "Rarely", "Never"], values: [4, 3, 2, 1] },
    { question: "Do you feel relaxed at home?", options: ["Always", "Often", "Sometimes", "Rarely"], values: [4, 3, 2, 1] },
];

let currentQuestionIndex = 0;
let totalScore = 0;
let childScore = 0;
const maxScore = questions.reduce((total, question) => total + 4, 0);
const childMaxScore = childQuestions.reduce((total, question) => total + 4, 0);

const startBtn = document.getElementById("start-btn");
const quizContainer = document.getElementById("quiz-container");
const questionElement = document.getElementById("question");
const optionButtons = document.querySelectorAll(".option-btn");
const resultContainer = document.getElementById("result");
const careScoreElement = document.getElementById("care-score");
const resultTips = document.getElementById("result-tips");
const askChildBtn = document.getElementById("ask-child-btn");

const childQuizContainer = document.getElementById("child-quiz-container");
const childQuestionElement = document.getElementById("child-question");
const childOptionButtons = document.querySelectorAll(".child-option-btn");
const childResultContainer = document.getElementById("child-result");
const childScoreElement = document.getElementById("child-score");
const childTips = document.getElementById("child-tips");
const consultExpertBtn = document.getElementById("consult-expert-btn");

// Start Parent Quiz
startBtn.addEventListener("click", () => {
    startBtn.style.display = "none";
    quizContainer.style.display = "block";
    showQuestion();
});

// Show next parent question
function showQuestion() {
    if (currentQuestionIndex < questions.length) {
        const currentQuestion = questions[currentQuestionIndex];
        questionElement.textContent = currentQuestion.question;
        optionButtons.forEach((button, index) => {
            button.textContent = currentQuestion.options[index];
            button.onclick = () => selectOption(index);
        });
    } else {
        showParentResult();
    }
}

// Handle parent option selection
function selectOption(index) {
    totalScore += questions[currentQuestionIndex].values[index];
    currentQuestionIndex++;
    showQuestion();
}

// Show parent result
function showParentResult() {
    quizContainer.style.display = "none";
    resultContainer.style.display = "block";
    const careScore = Math.round((totalScore / maxScore) * 100);
    careScoreElement.textContent = careScore;

    askChildBtn.style.display = "block"; // Always show the option to ask child questions
    
    if (careScore < 50) {
        resultTips.innerHTML = `<h3><u>Intensive Parenting Tips<u></h3>
                                <ul>
                                    <li>Spend more one-on-one quality time with your child to strengthen the bond.</li>
                                    <li>Be extra cautious about your child's emotional needs and provide consistent support.</li>
                                    <li>Engage in positive discipline techniques and avoid punitive actions.</li>
                                    <li>Foster a safe and nurturing environment for the child to express themselves.</li>
                                </ul>`;
    } else {
        resultTips.innerHTML = `<h3><u>General Parenting Tips<u></h3>
                                <ul>
                                    <li>Maintain a consistent schedule for spending time with your child.</li>
                                    <li>Encourage open communication by asking your child how they feel regularly.</li>
                                    <li>Introduce constructive activities such as creative games and educational tasks.</li>
                                    <li>Set boundaries while giving the child enough freedom to make decisions.</li>
                                </ul>`;
    }
}

// Start child quiz
askChildBtn.addEventListener("click", () => {
    resultContainer.style.display = "none";
    childQuizContainer.style.display = "block";
    currentQuestionIndex = 0;
    childScore = 0;
    showChildQuestion();
});

// Show next child question
function showChildQuestion() {
    if (currentQuestionIndex < childQuestions.length) {
        const currentQuestion = childQuestions[currentQuestionIndex];
        childQuestionElement.textContent = currentQuestion.question;
        childOptionButtons.forEach((button, index) => {
            button.textContent = currentQuestion.options[index];
            button.onclick = () => selectChildOption(index);
        });
    } else {
        showChildResult();
    }
}

// Handle child option selection
function selectChildOption(index) {
    childScore += childQuestions[currentQuestionIndex].values[index];
    currentQuestionIndex++;
    showChildQuestion();
}

// Show child result
function showChildResult() {
    childQuizContainer.style.display = "none";
    childResultContainer.style.display = "block";
    const childScorePercentage = Math.round((childScore / childMaxScore) * 100);
    childScoreElement.textContent = childScorePercentage;

    if (childScorePercentage < 50) {
        childTips.style.display = "none";
        consultExpertBtn.style.display = "block";
    } else {
        consultExpertBtn.style.display = "none";
        childTips.style.display = "block";
        childTips.innerHTML = `<h3>Child Well-being Tips</h3>
                               <ul>
                                   <li>Ensure your child feels safe and supported.</li>
                                   <li>Encourage your child to express their emotions.</li>
                                   <li>Foster healthy friendships and social connections.</li>
                                   <li>Monitor your child's mental well-being regularly.</li>
                               </ul>`;
    }
}
