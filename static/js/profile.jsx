// function ImgData(props) {
//     return (
//       <div style= {{display:"inline-block", margin: "10px"}}className="img">
//         <img style={{boxShadow: "5px 5px 5px 5px grey", width:"50%", height:"auto"}}  src={props.img_location} />
//         <p style= {{fontSize: "20"}}>{props.img_caption}</p>
//         <p style={{fontSize: "10"}}>{props.img_dateuploaded}</p>
//         <br></br>
//         <br></br>

//       </div>
//     );
//   }


function ImgData(props) {
  return (
    <div>
        <div class ="card" style={{width:"50rem", display:"block", marginLeft:"auto", marginRight:"auto"}}>
          <img src={props.img_location} class="img-thumbnail"/>
          <div class="card-body">
            <p class = "card-text" style= {{fontSize: "20"}}>{props.img_caption}</p>
            <p class = "card-text"style= {{fontSize: "5"}} >{props.img_dateuploaded}</p>
          </div>
        </div>
        <br></br>
    </div>
  );
}
  
function ImgContainer() {
    const [images, updateImgs] = React.useState([]);

    React.useEffect(() => {
        fetch('/api/profile_data')
        .then((response) => response.json())
        .then((data) => updateImgs(data))
    }, [])

    const imglist = [];

    for (const currentImg of images) {
        imglist.push(
        <ImgData
            img_location={currentImg.img_location}
            img_dateuploaded={currentImg.date_uploaded}
            img_caption = {currentImg.caption}
        />
        );
    }

    return (<div>{imglist}</div>);

}


function Username(){
  return (<h1 style={{fontSize:"20px", textAlign:"left"}} >Welcome to your profile page {username} </h1>)
}


ReactDOM.render(<div> 
                <Username /> <br></br>
                <ImgContainer /> 
                </div>, document.getElementById('root'));
