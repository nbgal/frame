 function ImgData(props) {
    
    console.log(props.img_comments)
    const comments = props.img_comments
    return (
    <div>
        <div className ="card" style={{width:"40rem", display:"block", marginLeft:"auto", marginRight:"auto", backgroundColor:"#edf2fb", padding:"6px"}}>

            <p className ="card-header-top" style={{display: "inline-block", fontSize:"15", float:"left", marginTop:"1rem"}}> 
                <img className="commenter_image" src={props.follower_profile_img} />
                <span> {props.follower_firstname} {props.follower_lastname} </span>
            </p>

            <button style={{display:"inline-block", float:"right", color:"#007bff", fontWeight:"light", marginTop:"0.5rem"}} className ="card-header-top btn btn-link" onClick={()=>props.handleOnClick(props.follower_id)}>Unfollow</button>

           
            <img src={props.img_location} className ="img-thumbnail" style={{backgroundColor:"white"}}/>

            <div className="card-body" style={{paddingBottom:"0px"}}>
                <p className = "card-text" style= {{fontSize: "20"},{textAlign:"center"}}>{props.img_caption}</p>
                <p className = "card-text" style= {{fontSize: "7"}} >{props.img_dateuploaded}</p>
                <p className= "card-text" style= {{fontSize: "15px", font:"Georgia", textAlign:"left"}}  >
                    {comments.map(({commenter_id, commenter_firstname, commenter_lastname, comment_text, commenter_profile_img}) => {
                      return(
                        <p key = {commenter_id}>
                          <img className="commenter_image" src={commenter_profile_img} />
                          <span> {commenter_firstname} {commenter_lastname}: {comment_text} </span>
                        </p>
                    )})}
                      <br></br>
                </p>
            </div>

            <form class="card-body modal-content" style={{backgroundColor:"#edf2fb", padding:"0px", border:"0px", marginBottm:"0px"}} onSubmit={props.handleSubmit}>
                <label >
                <textarea class="modal-content textarea.form-control font" name="Comment" placeholder="Add a comment.." /></label>
                <input type="hidden" name="img_id" value={props.img_id}/>
                <input class="btn btn-link" style={{float:"right"}} type ="submit" value="Post"/>
            </form>
        </div>
        <br></br><br></br>     
    </div>
);
}



function ImgContainer() {
    const [images, updateImgs] = React.useState([]);
    

    function FetchData(){
        fetch('/api/newsfeed_data')
        .then((response) => response.json())
        .then((data) => updateImgs(data))
    }
    React.useEffect(() => FetchData(), [])

    // This function handles deleting a user
    function handleOnClick(follower_id) 
    {
        
        const answer = fetch(`/unfollow/${follower_id}`, {
            method: "DELETE",
            headers: {
                'Content-Type': 'application/json'},
            // body: JSON.stringify({follower_id: xx , username: xx}),
            mode: "same-origin"
        }).then((answer) =>  FetchData())
    } //End of function


        // This function handles adds a comment
        function handleSubmit(event) 
        {
            const data = new FormData(event.target)
    
            if (data.get("Comment") == ""){
                pass;
            }
            else{
                const response = fetch('/addcomment', {
                    method: "post",
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({img_id: data.get("img_id") , Comment: data.get("Comment"), }),
                    mode: "same-origin"
                }).then((response) => console.log(response))}
        }



    const imglist = [];

    for (const currentImg of images) {
        imglist.push(
        <ImgData
            follower_id={currentImg.follower_id}
            follower_profile_img= {currentImg.follower_profile_img}
            follower_firstname={currentImg.follower_firstname}
            follower_lastname={currentImg.follower_lastname}
            img_id={currentImg.img_id}
            img_location={currentImg.img_location}
            img_dateuploaded={currentImg.img_dateuploaded}
            img_caption = {currentImg.caption}
            handleOnClick={handleOnClick}
            handleSubmit={handleSubmit}
            img_comments={currentImg.comment_data}
        />
        );
    }

    return (<div>{imglist}</div>);

}

// function Username(){
//   return (<h2 style={{fontSize:"20px", textAlign:"center"}} >Welcome to your Newsfeed {username} </h2>)
// }


ReactDOM.render(<div> 
   <br></br><br></br>
    <ImgContainer /> 
    </div>, document.getElementById('root'));
