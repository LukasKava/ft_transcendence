
import React, { useRef, useState, useEffect, forwardRef, useContext } from 'react';
import { Canvas, useFrame, useLoader} from '@react-three/fiber';
import { OrbitControls, Edges, RoundedBox } from '@react-three/drei';
import { useTranslation } from "react-i18next";
import { AccessibilityContext } from '../../AccessibilityContext';
import { postMatchResults } from '../../services/postMatchResults';
import { GameContext } from "../../context/GameContext";
import '../game/controlPanel.css'
import '../game/gameStartMenu.css'
import WinningScreen from './WinningScreen';
import { t } from 'i18next';

let 	FIELD_WIDTH         = 26;
let 	FIELD_LEN           = 32;
let 	FIELD_HALF_WIDHT    = FIELD_WIDTH / 2;
let 	FIELD_HALF_LEN      =  FIELD_LEN / 2;

const	PLAYER_SPEED        = 0.5;
const	PLAYER_WIDTH        = 4;
const	PLAYER_LEN          = 1;
const	PLAYER_HALF_WIDTH   = PLAYER_WIDTH / 2;
const	PLAYER_HALF_LEN     = PLAYER_LEN / 2;

const	PLAYER_ONE_COLOR    = "#FFFFFF";
const	PLAYER_TWO_COLOR    = "#60616D";

const   STARTING_BALL_SPEED = 0.12;
const	MAX_BALL_SPEED      = 0.23;
let		BALL_SPEED          = 0.12;
const	BALL_RADIUS         = 0.7;

const 	MAX_SCORE_COUNT     = 3;
const 	MAX_SET_COUNT       = 0; //dev


function Ball({player1Ref, player2Ref, handleScore}) {
	//Reference to the ball mesh
	const meshRef = useRef();

	//Refs to store position and velocity without causing re-renders
	const velocity = useRef([0.1, 0, 0.1]); 
	const position = useRef([0, 1, 0]); //Initial position

	const hasCollided = useRef(false);

	const calculateBallReflectionAndUpdateVelocity = (ball, player) => {
		const ballPos = ball.position.x;
		const playerPos = player.position.x;

		let collisionPoint = ballPos - playerPos;

		//Normalize to range [-1, 1]
		collisionPoint = collisionPoint / 2;

		//Calculate the angle of reflection
		const angleRad = (Math.PI / 4) * collisionPoint;

		//Determine direction based on ball position (top or bottom of the field)
		const direction = ball.position.z > 0 ? 1 : -1;

		velocity.current[2] = -direction * BALL_SPEED * Math.cos(angleRad); //Forward/backward
		velocity.current[0] = BALL_SPEED * Math.sin(angleRad); 				//Sideways

		if (BALL_SPEED <= MAX_BALL_SPEED) {
			BALL_SPEED += 0.01;
		}
		// console.log("BALL SPEED NORMALLY: ", BALL_SPEED);
	};


	const checkCollisionAABB = (playerRef) => {
		if (!playerRef.current) return false;

		const playerPos = playerRef.current.position;

		//Bounding box collision detection
		const ballX = position.current[0];
		const ballZ = position.current[2];

		//Check if the ball is within the player's boundaries
		//Axis-Aligned Bounding Box (AABB) Collision Detection
		//Used for the plane of x z 
		return (
			ballX >= playerPos.x - PLAYER_HALF_WIDTH - BALL_RADIUS &&
			ballX <= playerPos.x + PLAYER_HALF_WIDTH + BALL_RADIUS &&
			ballZ >= playerPos.z - PLAYER_HALF_LEN - BALL_RADIUS &&
			ballZ <= playerPos.z + PLAYER_HALF_LEN + BALL_RADIUS
		);
	};

	useFrame(() => {
    	if (!meshRef.current) return;

    	//Calculate the new position
    	const [vx, vy, vz] = velocity.current;
    	const [px, py, pz] = position.current;
    	const newPosition = [px + vx, py + vy, pz + vz];
    	const halfWidth = (FIELD_WIDTH - 2 - BALL_RADIUS) / 2;
    	const halfLength = (FIELD_LEN - 1) / 2;

    	if (newPosition[0] > halfWidth || newPosition[0] < -halfWidth) {
    	  velocity.current[0] = -vx; //Reverses it
    	}

		const collidedWithPlayer1 = checkCollisionAABB(player1Ref);
		const collidedWithPlayer2 = checkCollisionAABB(player2Ref);

		//GOAL
		if ((newPosition[2] + BALL_RADIUS) > (halfLength - PLAYER_LEN) & 
			 collidedWithPlayer2 === false) {
			// alert("GOAL1");
			handleScore(2);
			position.current = [0, 1, 0];
			velocity.current = [0.1, 0, 0.1];
			return;
		} else if ((newPosition[2] - BALL_RADIUS) < (-halfLength + PLAYER_LEN) &
					collidedWithPlayer1 === false) {
			// alert("GOAL2");
			handleScore(1);
			position.current = [0, 1, 0];
			velocity.current = [0.1, 0, -0.1];
			return;
		}

		//Player collision detection
		if ((collidedWithPlayer1 || collidedWithPlayer2) && !hasCollided.current) {
			const playerRef = collidedWithPlayer1 ? player1Ref : player2Ref;

			calculateBallReflectionAndUpdateVelocity(meshRef.current, playerRef.current);
			hasCollided.current = true;
		} else if (!collidedWithPlayer1 && !collidedWithPlayer2) {
			hasCollided.current = false;
		}

		position.current = newPosition; 																/*Update ball position          */
		meshRef.current.position.set(...newPosition);													/*Apply the position to the mesh*/
			
	});
	return (
		<mesh ref={meshRef}>
    		<sphereGeometry args={[0.7, 32, 32]} />
    		<meshStandardMaterial color="orange" />
    	</mesh>
	);
}

const Player = forwardRef(({ position, color, controls }, ref) => {
	const meshRef = useRef();
  
	const keysPressed = useRef({});
  
	useEffect(() => {
		const handleKeyDown = (e) => {
			keysPressed.current[e.key] = true;
	  	};
  
		const handleKeyUp = (e) => {
			keysPressed.current[e.key] = false;
		};
  
		window.addEventListener('keydown', handleKeyDown);
		window.addEventListener('keyup', handleKeyUp);
  
		return () => {
			window.removeEventListener('keydown', handleKeyDown);
			window.removeEventListener('keyup', handleKeyUp);
	  	};
	}, []);
  
	useFrame(() => {
  
		//Updating the meshRef position
		if (meshRef.current) {
			if (meshRef.current.position.x - PLAYER_HALF_WIDTH > -FIELD_HALF_WIDHT + 1) {
				if (keysPressed.current[controls.left]) meshRef.current.position.x -= PLAYER_SPEED; //Move left
			}
			if(meshRef.current.position.x + PLAYER_HALF_WIDTH < FIELD_HALF_WIDHT - 1) {
				if (keysPressed.current[controls.right]) meshRef.current.position.x += PLAYER_SPEED; //Move right
			}
	  	}

		if (ref) ref.current = meshRef.current;
	});
	return (	
		<mesh ref={meshRef} position={position}>
			<RoundedBox args={[4, 1, 1]} radius={0.2} smoothness={4}>
				<meshStandardMaterial color={color} />
			</RoundedBox>
		</mesh>
	);

});
  


function Field({dimensions, borderColor, gameFieldStyle}) {
	const wallThickness = 0.1;

	return (
		<>
		{/*FIELD PICTURE OPTION 1*/}
		{gameFieldStyle === "option2" && (
			<mesh position={[0, -3, 0]} rotation={[-Math.PI / 2, 0, 0]}>
				<boxGeometry args={[FIELD_WIDTH - 8, FIELD_LEN - 8, 5]} />
				<meshStandardMaterial color={PLAYER_ONE_COLOR} transparent={true} opacity={0.1}/>
				{/* Edge Outline */}
				<Edges threshold={1} color="#6E4E59" />
			</mesh>
		)}
    	{/* Border walls */}
    	{/* Left Wall */}
    	<mesh position={[-dimensions.width / 2 - wallThickness / 2, 0, 0]}>
    		<boxGeometry args={[wallThickness, dimensions.height, dimensions.length - 4]} />
    		<meshStandardMaterial color={borderColor} />

    	</mesh>

    	{/* Right Wall */}
    	<mesh position={[dimensions.width / 2 + wallThickness / 2, 0, 0]}>
    		<boxGeometry args={[wallThickness, dimensions.height, dimensions.length - 4]} />
    		<meshStandardMaterial color={borderColor} />
    	</mesh>

    	{/* Top Wall */}
    	<mesh position={[0, 0, dimensions.length / 2 + wallThickness / 2]}>
    		<boxGeometry args={[dimensions.width - 4, dimensions.height, wallThickness]} />
    	  	<meshStandardMaterial color={borderColor} />
    	</mesh>

    	{/* Bottom Wall */}
    	<mesh position={[0, 0, -dimensions.length / 2 - wallThickness / 2]}>
    		<boxGeometry args={[dimensions.width - 4, dimensions.height, wallThickness]} />
    		<meshStandardMaterial color={borderColor} />
    	</mesh>
		{/* Middle Wall */}
		<mesh position={[0, 0, 0]}>
    		<boxGeometry args={[dimensions.width - 4, dimensions.height, 0.05]} />
    		<meshStandardMaterial color={borderColor} />
    	</mesh>
    	</>
  	);
}


function ControlPanel() {
	const ChangeStyle = () => {
		// alert("Great Shot!");
		let changeStyle = document.getElementById("changeStyle");
		if (changeStyle.style.fontWeight === "200") {
			changeStyle.style.fontWeight =  "400";
		} else {
			changeStyle.style.fontWeight = "200";
		}
	};
	const KeyboardControls = () => {
		// alert("1");
		let keyboardControls = document.getElementById("keyboardControls");
		if (keyboardControls.style.fontWeight === "200") {
			keyboardControls.style.fontWeight =  "400";
		} else {
			keyboardControls.style.fontWeight = "200";
		}
	};
	const LeaveGame = () => {
		// alert("2");
		let leaveGame = document.getElementById("leaveGame");
		if (leaveGame.style.fontWeight === "200") {
			leaveGame.style.fontWeight =  "400";
		} else {
			leaveGame.style.fontWeight = "200";
		}
	};

	const ControlPanelMenu = () => {
		// console.log("Turn on the menu");
		let choices = document.getElementById("choiseMenu");
		if (choices.style.display !== "none") {
			choices.style.display = "none";
		} else {
			choices.style.display = "flex";
		}

	}
	return (
		<div style={{position: 'absolute', top: '50%', right: '5rem', display: 'flex', alignItems: 'center', flexDirection: 'row', gap: '2.5rem', zIndex:100}}>
		{/* <div style={{position: 'absolute', top: '50%', right: '5rem', border: '1px solid red', display: 'flex', alignItems: 'center', flexDirection: 'row', gap: '2rem'}}> */}
			<div id="choiseMenu" style={{ fontSize: '18px', display: 'flex', flexDirection: 'column', gap: '1.5rem', height: '4rem', justifyContent: 'center'}}>
			{/* <div style={{border: '1px solid green', fontSize: '18px', display: 'flex', flexDirection: 'column', gap: '1.5rem'}}> */}
				<button id="changeStyle" className="controlPanelButton" onClick={ChangeStyle}>
					Change Style
				</button>
				<button id="keyboardControls" className="controlPanelButton" style={{}} onClick={KeyboardControls}>
					Keyboard Controls
				</button>
				<button id="leaveGame" className="controlPanelButton" style={{}} onClick={LeaveGame}>
					Leave Game
				</button>
			</div>
			<div style={{ width: '2.2rem', height: '4rem', border:'1.5px solid white', display: 'flex', justifyContent: 'center', borderRadius: '18%'}} onClick={ControlPanelMenu}>
				<div style={{display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', gap: '0.4rem'}}>
					<div style={{width: '0.4rem', height: '0.4rem', backgroundColor: 'white', borderRadius: '100%'}}></div>
					<div style={{width: '0.4rem', height: '0.4rem', backgroundColor: 'white', borderRadius: '100%'}}></div>
					<div style={{width: '0.4rem', height: '0.4rem', backgroundColor: 'white', borderRadius: '100%'}}></div>
				</div>
			</div>
		</div>

	);
}

function PlayerPanel({scores}) {
	const { player1DisplayName, player2DisplayName } = useContext(GameContext);

	return (
		<div style={{ position: 'absolute', top: '5rem', left: '50%', transform: 'translateX(-50%)', color: 'white', fontSize: '24px' }}>
			{player1DisplayName}: {scores.p1_in_set_score} {t("Set count")}: {scores.p1_won_set_count} | {player2DisplayName}: {scores.p2_in_set_score} {t("Set count")}: {scores.p2_won_set_count}
		</div>
	);
}


function GameStartMapMenu() {
	const [selectedOption, setSelectedOption] = useState("normal");
	const { t } = useTranslation();

    const options = [t("normal"), t("wide"), t("narrow")];

	if (selectedOption === "normal") {
		FIELD_WIDTH = 26;
		FIELD_LEN = 32;
		FIELD_HALF_WIDHT = FIELD_WIDTH / 2;
		FIELD_HALF_LEN =  FIELD_LEN / 2;
	} else if (selectedOption === "wide") {
		FIELD_WIDTH = 40;
		FIELD_LEN = 32;
		FIELD_HALF_WIDHT = FIELD_WIDTH / 2;
		FIELD_HALF_LEN =  FIELD_LEN / 2;
	} else if (selectedOption === "narrow") {
		FIELD_WIDTH = 20;
		FIELD_LEN = 32;
		FIELD_HALF_WIDHT = FIELD_WIDTH / 2;
		FIELD_HALF_LEN =  FIELD_LEN / 2;
	}

    return (
        <div id="menu">
            {options.map((option) => (
                <div	key={option}
						className={`menuChoiceElement option ${selectedOption === option ? "selected" : ""}`}
						onClick={() => setSelectedOption(option)}
						style={{ fontWeight: selectedOption === option ? "bold" : "normal", cursor: "pointer" }}
                >
                    <p>{selectedOption === option ? "→ " : ""}{option}</p>
                </div>
            ))}
        </div>
    );
}

function GameStartStylesMenu({gameFieldStyle, setGameStyle}) {
	// const [selectedOption, setSelectedOption] = useState("normal");
	const { t } = useTranslation();

    const options = [t("normal"), t("option2")];

    return (
        <div id="menu">
            {options.map((option) => (
                <div	key={option}
						className={`menuChoiceElement option ${gameFieldStyle === option ? "selected" : ""}`}
						onClick={() => setGameStyle(option)}
						style={{ fontWeight: gameFieldStyle === option ? "bold" : "normal", cursor: "pointer" }}
                >
                    <p>{gameFieldStyle === option ? "→ " : ""}{option}</p>
                </div>
            ))}
        </div>
    );
}

function GameStartMenu({onStartGame, gameFieldStyle, setGameStyle}) {
	const { t } = useTranslation();

	return (
		<div id="gameStartMenu">
			<h2>{t("Welcome to the game start menu")}</h2>
			<div id="gameMenuArea1">
				<div id="gameMenuElementWrapper">
					<div id="choiceArea">
						<h2 className="gameStartMenuH2">{t("Choices")}</h2>
						<div className="choiceAreaSections">
							<div>
								<h3 className="gameStartMenuH3">{t("Map")}</h3>
								<GameStartMapMenu/>
							</div>
							<div>
								<h3 className="gameStartMenuH3">{t("Styles")}</h3>
								<GameStartStylesMenu gameFieldStyle={gameFieldStyle} setGameStyle={setGameStyle}/>
							</div>
						</div>
					</div>
					<div id="controlsArea">
						<h2 className="gameStartMenuH2">{t("Keyboard Controls")}</h2>
						<div id="p1Controls">
							<h3 className="gameStartMenuH3">P1</h3>
							<div className="pControlsWrapper">
								<div className="p1Keys">A</div><div className="p1Keys"></div><div className="p1Keys">D</div>
							</div>
						</div>
						<div id="p2Controls">
							<h3 className="gameStartMenuH3">P2</h3>
							<div className="pControlsWrapper">
								<div className="p2Keys">&lt;</div><div className="p2Keys"></div><div className="p2Keys">&gt;</div>
							</div>
						</div>
					</div>
				</div>
			</div>
			<button className="btn button" onClick={onStartGame}>{t("Start Game")}</button>
		</div>
	);
}

function Pong() {
	// disableNavigationButtons();
// Declare refs inside the Canvas component
	const { player1Id,
			player2Id,
			iDTournamentGame,
			player1DisplayName, 
			player2DisplayName } = useContext(GameContext);

	const { t } = useTranslation();
	const player1Ref = useRef();
	const player2Ref = useRef();
	const [gameStarted, setGameStarted] = useState(false);
	const [gameFieldStyle, setGameStyle] = useState("normal");
	const [winner, setWinner] = useState(null);
	BALL_SPEED = STARTING_BALL_SPEED;

// console.log("match Id rn: ", iDTournamentGame);
	const [scores, setScores] = useState({
		p1_f_score: 0,
		p2_f_score: 0,
		p1_in_set_score: 0,
		p2_in_set_score: 0,
		p1_won_set_count: 0,
		p2_won_set_count: 0,
	});
	
	const handleScore = (player) => {
		setScores((prev) => {
		  const updatedScores = { ...prev };
		  if (player === 1) {
			updatedScores.p1_f_score++;
			updatedScores.p1_in_set_score++;
			if (updatedScores.p1_in_set_score >= MAX_SCORE_COUNT) {
				updatedScores.p1_in_set_score = 0; // Reset score for next set
				updatedScores.p1_won_set_count++;
				if (updatedScores.p1_won_set_count >= MAX_SET_COUNT) {
					// alert('Player 1 has won the game!');
					//SEND THE STATISTICAL DATA BACK TO THE DATABASE
					postMatchResults(player1Id, updatedScores, iDTournamentGame, player1Id, player2Id);
					setWinner(player1DisplayName ? player1DisplayName : t("Player 1"));
				}
			}
		  } else if (player === 2) {
			updatedScores.p2_f_score++;
			updatedScores.p2_in_set_score++;
			if (updatedScores.p2_in_set_score >= MAX_SCORE_COUNT) {
				updatedScores.p2_in_set_score = 0; // Reset score for next set
				updatedScores.p2_won_set_count++;
				if (updatedScores.p2_won_set_count >= MAX_SET_COUNT) {
					// alert('Player 2 has won the game!');
					//SEND THE STATISTICAL DATA BACK TO THE DATABASE
					postMatchResults(player2Id, updatedScores, iDTournamentGame, player1Id, player2Id);
					setWinner(player2DisplayName ? player2DisplayName : t("Player 2"));
				}
			}
		  }
		  return updatedScores;
		});
	};

	const handleStartGame = () => {
        const menu = document.getElementById("gameStartMenu");
        if (menu) {
            menu.style.opacity = "0"; // Fade out animation
            setTimeout(() => setGameStarted(true), 500); // Wait 0.5s before starting game
        } else {
            setGameStarted(true);
			// console.log("ERROR: in handleStartGame function !");
        }
    };

	if (winner) {
		return <WinningScreen player={winner} score1={scores.p1_f_score} score2={scores.p2_f_score}/>
	}
	if (gameStarted === false) {
		// console.log("Start of the game ball speed: ", BALL_SPEED);
		return (<div id="pong-container" style={{ width: '100vw', height: '100vh', /*marginTop: '20px'*/}}>
			<GameStartMenu onStartGame={handleStartGame} gameFieldStyle={gameFieldStyle} setGameStyle={setGameStyle}/>
		</div>);
	}


	return (
	<div id="pong-container" style={{ width: '100vw', height: '100vh', /*marginTop: '50px',*/ zIndex:'2000'}}  >

		{/* <ControlPanel/> */}
		<PlayerPanel scores={scores}/>
		<Canvas style={{width: '99vw', height: '99vh', zIndex: 10}} camera={{ fov: 75, near: 0.1, far: 200, position: [0, 100, 150] }}>
			{/* <axesHelper args={[15]} /> */}
			<OrbitControls
				enableZoom={true}  
				enablePan={true}
				maxPolarAngle={Math.PI / 2}
				minDistance={5}
				maxDistance={30}
				makeDefault
			/>
			<ambientLight intensity={Math.PI / 2} />
			<spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} decay={0} intensity={Math.PI} />
			<pointLight position={[-10, -10, -10]} decay={0} intensity={Math.PI} />
			<Field dimensions={{width: FIELD_WIDTH - 2, height: 0.1, length: FIELD_LEN - 2}} position={[0, 0, 0]} color="#0E0F22" borderColor="white" gameFieldStyle={gameFieldStyle}/>

			<Ball player1Ref={player1Ref} player2Ref={player2Ref} handleScore={handleScore}/>
			<Player
				position={[0, 1, FIELD_LEN / 2 - 1.5]}
				color={PLAYER_ONE_COLOR}
				controls={{ left: 'a', right: 'd' }}
				ref={player1Ref}
			/>
			<Player
				position={[0, 1, -FIELD_LEN / 2 + 1.5]}
				color={PLAYER_TWO_COLOR}
				controls={{ left: 'ArrowLeft', right: 'ArrowRight' }}
				ref={player2Ref}
			/>
		</Canvas>
	</div>
	);
  }
  
//   createRoot(document.getElementById('root')).render(<MyCanvas />);
export default Pong;