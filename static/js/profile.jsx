function ImgData(props) {

  const comments = props.img_comments;

  return (
    <div>
          <input type="image" className={"gallery__img__"+props.img_orientation} data-toggle="modal" data-target={"#myModal"+props.img_id} src= {props.img_location}></input>
          <div className="modal fade" id={"myModal"+props.img_id} tabIndex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
            <div className="modal-dialog modal-dialog-centered">
              <div className="modal-content">
                <div class="modal-header">
                  <button type="button" class="close" data-dismiss="modal">×</button>
                </div>
                               
                <div className="modal-body">
                  <img src={props.img_location} style={{width:"100%"}}/>
                  <p className = "font" style= {{fontSize: "20px"}}>{props.img_caption}</p>
                  <p className = "font" style= {{fontSize: "7px"}}>{props.img_dateuploaded}</p>
                </div>
                      
                <div>
                  <p style= {{fontSize: "15px", font:"Georgia", textAlign:"left"}}  >
                    {comments.map(({commenter_id, commenter_firstname, commenter_lastname, comment_text, commenter_profile_img}) => {
                      return(
                        <ul key = {commenter_id}>
                          <img className="commenter_image" src={commenter_profile_img} />
                          <span> {commenter_firstname} {commenter_lastname}: {comment_text} </span>
                        </ul>
                    )})}
                      <br></br>
                  </p>
                </div>

                <form class="modal-content" onSubmit={props.handleSubmit}>
                  <label style= {{fontSize:"10"}}>
                  <textarea class="modal-content textarea.form-control font" name="Comment" placeholder="Add a comment.." /></label>
                  <input type="hidden" name="img_id" value={props.img_id}/>
                  <input className="btn btn-link" style={{float:"right", border:"0px"}} type ="submit" value="Post"/>
                </form>
              </div>
                        
            </div>
          </div>
      </div>
  );
}
  
function ImgContainer() {
  const [images, updateImgs] = React.useState([]);

  function FetchData(){
    fetch('/api/profile_data')
    .then((response) => response.json())
    .then((data) => updateImgs(data))
  }
  React.useEffect(() => FetchData(), [])

    // React.useEffect(() => {
    //     fetch('/api/profile_data')
    //     .then((response) => response.json())
    //     .then((data) => updateImgs(data))
    // }, [])

  function handleSubmit(event) {
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
            key = {currentImg.img_id}
            img_id={currentImg.img_id}
            img_location={currentImg.img_location}
            img_dateuploaded={currentImg.date_uploaded}
            img_caption = {currentImg.caption}
            img_comments= {currentImg.comments}
            img_orientation= {currentImg.img_orientation}
            handleSubmit={handleSubmit}
            

        />
        );
    }

    return (<div className = "gallery">{imglist}</div>);

}


function UserProfile(){

  const [userData, updateData] = React.useState([]);

    React.useEffect(() => {
        fetch('/api/user_profile_data')
        .then((response) => response.json())
        .then((data) => updateData(data))
    }, [])
  return (
      <div>
        <br></br>
        <img  src ={userData.user_profile_img}  className= "rounded-circle profile_image mx-auto d-block" ></img>
        <br></br>
        <h1 style={{fontSize:"15px", textAlign:"center", fontFamily: "Georgia", fontWeight:"bold"}} > {userData.user_firstname} {userData.user_lastname}</h1>
        <h2 style={{fontSize:"10px", textAlign:"center", fontFamily: "Georgia"}} > {userData.user_location}</h2>
        <hr></hr>
        </div>)
}

ReactDOM.render(<div> 
                <UserProfile /> <br></br>
                <ImgContainer /> 
                </div>, document.getElementById('root'));
