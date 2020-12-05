function UserContainer() {
    const [user, updateUserData] = React.useState([]);
    console.log("here")    

    function FetchData(){
        fetch('/api/search')
        .then((response) => response.json())
        .then((data) => updateUserData(data))
      }
    
    React.useEffect(() => FetchData(), [])


    function handleOnClick(status) 
    {
        if(status == "Unfollow"){
            const answer = fetch(`/unfollow/${user.user_id}`, {
                method: "DELETE",
                headers: {
                    'Content-Type': 'application/json'},
                // body: JSON.stringify({follower_id: xx , username: xx}),
                mode: "same-origin"
            }).then((answer) =>  FetchData())}
        else{
            const answer = fetch(`/follow/${user.user_id}`,{
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'},
                // body: JSON.stringify({follower_id: xx , username: xx}),
                mode: "same-origin"
                }).then((answer) =>  FetchData())}

            }

    var status = "Follow";

    if (user.followed==true){
        console.log("here")
        status = "Unfollow";
    }
    
    return (
        <div>
            <div className ="card" style={{width:"20rem", height:"auto", display:"block", marginLeft:"auto", marginRight:"auto", marginTop:"5vw", backgroundColor:"#edf2fb", padding:"6px", textAlign:"center",verticalAlign:"center"}}>

                <p className ="card-body" style={{display: "inline-block", fontSize:"15", marginTop:"1rem"}}> 
                
                    <img className= "rounded-circle profile_image mx-auto d-block" src={user.user_profile_img} />
                    <br></br>
                    <h2 style={{fontSize:"20px", textAlign:"center", fontFamily: "Georgia"}}> {user.user_firstname} {user.user_lastname} </h2>
                    <h3 style={{fontSize:"15px", textAlign:"center", fontFamily: "Georgia"}} > {user.user_location}</h3>
                    <button style={{fontSize:"15px", textAlign:"center", fontFamily: "Georgia"}} onClick={()=>handleOnClick(status)} > {status} </button>
                </p>
            </div>
          </div>
          );
}


ReactDOM.render(<div> <UserContainer /> </div>, document.getElementById('root'));
