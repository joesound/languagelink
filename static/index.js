


//model 
async function getQuestions(page){
    let response = await fetch(`${local}api/questions?page=${page}`);
    let response_to_json = await response.json()
    return response_to_json
}

async function createQuestion(questionData){
    let response = await fetch(`${local}api/questions`,{
        method: 'POST',
        body: JSON.stringify(questionData)
    });
    let response_to_json = await response.json()
    return response_to_json
}

async function getComments(questionid){
    let response = await fetch(`${local}api/comments/${questionid}`);
    let response_to_json = await response.json()
    return response_to_json
}

async function postComment(commentData){
    let response = await fetch(`${local}api/comment`,{
        method: 'POST',
        body: JSON.stringify(commentData)
    });
    let response_to_json = await response.json()
    return response_to_json
}


//view
function createQuestionBlock(question){

    const questionTitle = question["title"]
    const questionContent = question["content"]
    // const questionCoverimg = question["coverimg"]
    const questionUser = question["username"]
    const questionUserid = question["userid"]
    const questionId = question["questionid"]

    const questionBlock = document.createElement("div")
    const userBlock = document.createElement("div")
    const titleBlock = document.createElement("div")
    const contentBlock = document.createElement("div")
    // const coverimg = document.createElement("img")

    const userTextblock = document.createTextNode(questionUser);
    const titleTextblock = document.createTextNode(questionTitle);
    const contentTextblock = document.createTextNode(questionContent);
    // coverimg.src = questionCoverimg

    questionBlock.className = "questionblock"
    questionBlock.id = questionId
    userTextblock.id = questionUserid
    titleBlock.className = "titleblock"
    contentBlock.className = "contentblock"
    // coverimg.className = "coverimg"

    userBlock.appendChild(userTextblock)
    // titleBlock.appendChild(coverimg)
    titleBlock.appendChild(userBlock)
    titleBlock.appendChild(titleTextblock)
    contentBlock.appendChild(contentTextblock)
    questionBlock.appendChild(titleBlock)
    questionBlock.appendChild(contentBlock)

    questionBlock.addEventListener("click", (event)=>{popUpmore(event.target.id)})

    return questionBlock
}


function popQuestionBlock(question){

    const questionComent = question["comment"]
    // const questionCoverimg = question["coverimg"]
    const questionUser = question["username"]
    const questionCommentid = question["commentid"]

    const commentBlock = document.createElement("div")
    const userBlock = document.createElement("div")
    const contentBlock = document.createElement("div")
    // const coverimg = document.createElement("img")

    commentBlock.id = questionCommentid
    commentBlock.className = "commentblock"
    contentBlock.className = "contentblock"
    // coverimg.className = "coverimg"

    const userTextblock = document.createTextNode(questionUser);
    const contentTextblock = document.createTextNode(questionComent);
    // coverimg.src = questionCoverimg

    // userBlock.appendChild(coverimg)
    userBlock.appendChild(userTextblock)
    contentBlock.appendChild(contentTextblock)
    commentBlock.appendChild(userBlock)
    commentBlock.appendChild(contentBlock)
    return commentBlock
}


//control

async function loadQuestions(page){
    questionData = await getQuestions(page)
    const get_obsev_element = document.querySelector(".observer");
    if (questionData.length === 0){
        return 0
    }
    const contentContainer = document.querySelector(".content-container");


    for (index in questionData["data"]){
        const questionTitle = questionData["data"][index]["title"]
        const questionContent = questionData["data"][index]["content"]
        const questionUser = questionData["data"][index]["username"]
        const questionUserid = questionData["data"][index]["userid"]
        const questionId = questionData["data"][index]["questionid"]

        singleData = {
            "title":questionTitle,
            "content":questionContent,
            "username":questionUser,
            "userid":questionUserid,
            "questionid":questionId
        }

        // const imageUrl = `http://d24k1fqdjhq740.cloudfront.net/${commentImage}`
        const renderBlock = createQuestionBlock(singleData)
        contentContainer.insertBefore(renderBlock, get_obsev_element)

    }
    nowPage = nextPage
    nextPage = questionData["nextPage"]
    if (nextPage != null){
        observer.observe(loadingObserver);
    }


}



async function popUpmore(questionid){
    observer.unobserve(loadingObserver);
    const commentModal = document.querySelector(".commentModal")
    commentModal.id = questionid + "-comment"
    commentModal.style.dispay = "block"
    const questionBlock = document.getElementById(questionid)
    console.log(questionid)
    const leaveCommentblock = document.createElement("div")
    const modalInput = document.createElement("input");
    const modalButtom = document.createElement("input");
    modalInput.type = "text";
    modalInput.className = "modalinput"; 
    modalButtom.type = "buttom";
    modalButtom.className = "modalbuttom"; 
    leaveCommentblock.className = "leavecommentblock"
    modalButtom.addEventListener("click", (event)={})
    leaveCommentblock.appendChild(modalInput)
    leaveCommentblock.appendChild(modalButtom)
    commentModal.appendChild(questionBlock)

    questionData = await getComments(questionid)
    if (questionData.length === 0){
        return 0
    }

    for (index in questionData["data"]){

        const questionContent = commentData["data"][index]["content"]
        const questionUser = commentData["data"][index]["username"]
        const questionUserid = commentData["data"][index]["userid"]


        singleData = {
            "content":questionContent,
            "username":questionUser,
            "userid":questionUserid,
        }

        commentBlock = popQuestionBlock(singleData)
        commentModal.appendChild(commentBlock)

    commentModal.appendChild(leaveCommentblock)

}}

async function questionPost(){
    const questionPosttitle = document.querySelector('.question-input-title');
    const questionPostcontent = document.querySelector('.question-input-content');
    data = {
        "title":questionPosttitle.value,
        "content":questionPostcontent.value,
        "userid":'11ecd992-86c7-5e15-8830-f0761cd11ee5'
    }

    resp = await createQuestion(data)
    
}

async function commentPost(){
    const commentModalblock = document.querySelector('.commentModal');
    const commentPostcontent = document.querySelector('.modalinput');
    data = {
        "questionid":commentModalblock.id,
        "content":commentPostcontent.value,
        "userid":'11ecd992-86c7-5e15-8830-f0761cd11ee5'
    }
    
    resp = await postComment(data)
}




//main
const local = "http://127.0.0.1:3000/"
var nowPage  = 0
var nextPage = 0

// var nowPagemodal  = 0
// var nextPagemodal = 0

const loadingObserver = document.querySelector('.observer');

const questionPostbuttom = document.querySelector('.question-buttom');
questionPostbuttom.addEventListener("click", (event)=>{questionPost()})
// const modalgObserver = document.querySelector('.observerModal');




const options = {
    root: null,
    rootMargin: "0px",
    threshold: 0.2
    };
const  callback = async ([entry]) => {
    // 當此圖片進入 viewport 時才載入圖片
    if (entry && entry.isIntersecting) { 
        // 載入圖片
        observer.unobserve(loadingObserver);
        loadQuestions(nextPage)
    };
}


// const  callbackModal = async ([entry]) => {
//     // 當此圖片進入 viewport 時才載入圖片
//     if (entry && entry.isIntersecting) { 
//         // 載入圖片
//         observer.unobserve(modalgObserver);
//         popUpmore(nextPagemodal)
//     };
// }



let observer = new IntersectionObserver(callback, options);
observer.observe(loadingObserver);

// let observerModal = new IntersectionObserver(callbackModal, options);
// observerModal.observe(modalgObserver);