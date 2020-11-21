 function ImgData(props) {
    return (
  <div>
        <div className ="card" style={{width:"50rem", display:"block", marginLeft:"auto", marginRight:"auto", backgroundColor:"linen"}}>
            <p className ="card-header-top" style={{display: "inline-block", fontSize:"15", verticalAlign:"text-bottom", float:"left"}}> {props.follower_firstname} {props.follower_lastname} </p>
            <button style={{display:"inline-block", float:"right", color:"gray", backgroundColor:"linen", fontWeight:"light"}} className ="card-header-top" onClick={()=>props.handleOnClick(props.follower_id)}>Unfollow</button>
            <img src={props.img_location} className ="img-thumbnail" style={{backgroundColor:"linen"}}/>
            <div className="card-body">
                <p className = "card-text" style= {{fontSize: "20"}}>{props.img_caption}</p>
                <p className = "card-text"style= {{fontSize: "10"}} >{props.img_dateuploaded}</p>
            </div>
        </div>
        <br></br>
        
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

    function handleOnClick(follower_id) {

        const answer = fetch(`/unfollow/${follower_id}`, {
            method: "DELETE",
            headers: {
                'Content-Type': 'application/json'},
            // body: JSON.stringify({follower_id: xx , username: xx}),
            mode: "same-origin"
        }).then((resonse) =>  FetchData())
    }


    const imglist = [];

    for (const currentImg of images) {
        imglist.push(
        <ImgData
            follower_id={currentImg.follower_id}
            follower_firstname={currentImg.follower_firstname}
            follower_lastname={currentImg.follower_lastname}
            img_id={currentImg.img_id}
            img_location={currentImg.img_location}
            img_dateuploaded={currentImg.img_dateuploaded}
            img_caption = {currentImg.caption}
            handleOnClick={handleOnClick}
        />
        );
    }

    return (<div>{imglist}</div>);

}

function Username(){
  return (<h2 style={{fontSize:"20px", textAlign:"left"}} >Welcome to your newsfeed {username} </h2>)
}


ReactDOM.render(<div> 
    <Username /> <br></br>
    <ImgContainer /> 
    </div>, document.getElementById('root'));
