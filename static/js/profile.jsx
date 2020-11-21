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

  // const commentlist = props.comments;

  return (
    <div>
        {/* <div class ="card" style={{width:"50rem", display:"block", marginLeft:"auto", marginRight:"auto"}}>
          <img src={props.img_location} class="img-thumbnail"/>
          <div class="card-body">
            <p class = "card-text" style= {{fontSize: "20"}}>{props.img_caption}</p>
            <p class = "card-text"style= {{fontSize: "5"}} >{props.img_dateuploaded}</p>
          </div>
        </div> */}

          <input type="image" class="img-thumbnail1" data-toggle="modal" data-target={"#bd-example-modal-lg"+props.img_id} src= {props.img_location}></input>

          <div class="modal fade" id={"bd-example-modal-lg"+props.img_id} tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel" aria-hidden="true">
          <div class="modal-dialog modal-lg">
            <div class="modal-content">
                        
                        {/* <div class="modal-header">
                        <h4 class="modal-title">Modal Heading</h4>
                        <button type="button" class="close" data-dismiss="modal">×</button>
                        </div>
                         */}
                        
                        <div class="modal-body">
                          <img src={props.img_location} style={{width:"100%"}}/>
                          <p class = "card-text" style= {{fontSize: "20"}}>{props.img_caption}</p>
                          <p class = "card-text"style= {{fontSize: "5"}} >{props.img_dateuploaded}</p>
                          {/* <ul>
                            {commentlist.map((comment) =>
                              <ListItem value={comment} />
                            )}
                          </ul> */}
                          
              
                        </div>
                        
                    </div>
                    </div>
                </div>
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
    const commentList =[]

    for (const currentImg of images) {
        imglist.push(
        <ImgData
          
            img_id= {currentImg.img_id}
            img_location={currentImg.img_location}
            img_dateuploaded={currentImg.date_uploaded}
            img_caption = {currentImg.caption}
        />
        );
    }

    return (<div style={{display: "inline-block"}}>{imglist}</div>);

}


function Username(){
  return (<h1 style={{fontSize:"20px", textAlign:"left"}} >Welcome to your profile page {username} </h1>)
}


ReactDOM.render(<div> 
                <Username /> <br></br>
                <ImgContainer /> 
                </div>, document.getElementById('root'));
