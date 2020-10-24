function ImgData(props) {
    return (
  <div>
        <div class ="card" style={{width:"50rem", display:"block", marginLeft:"auto", marginRight:"auto", backgroundColor:"linen"}}>
            <p class ="card-header-top" style={{display: "inline-block", fontSize:"10", verticalAlign:"text-bottom"}}> {props.poster_firstname} </p>
            <button style={{display:"inline-block"}} class="card-header-top" onClick={handleOnClick}>Unfollow</button>
            <img src={props.img_location} class="img-thumbnail" style={{backgroundColor:"linen"}}/>
            <div class="card-body">
                <p class = "card-text" style= {{fontSize: "20"}}>{props.img_caption}</p>
                <p class = "card-text"style= {{fontSize: "10"}} >{props.img_dateuploaded}</p>
            </div>
        </div>
        <br></br>
    </div>

);
}

function handleOnClick() {

    console.log("clicked") 
}


function ImgContainer() {
    const [images, updateImgs] = React.useState([]);

    React.useEffect(() => {
        fetch('/api/newsfeed_data')
        .then((response) => response.json())
        .then((data) => updateImgs(data))
    }, [])

    const imglist = [];

    for (const currentImg of images) {
        imglist.push(
        <ImgData
            poster_firstname={currentImg.poster_firstname}
            poster_lastname={currentImg.poster_lastname}
            img_location={currentImg.img_location}
            img_dateuploaded={currentImg.img_dateuploaded}
            img_caption = {currentImg.caption}
        />
        );
    }

    return (<div>{imglist}</div>);

}


function Username(){
  return (<h1 style={{fontSize:"20px", textAlign:"left"}} >Welcome to your newsfeed {username} </h1>)
}


ReactDOM.render(<div> 
                <Username /> <br></br>
                <ImgContainer /> 
                </div>, document.getElementById('root'));
