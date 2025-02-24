import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import './Header.css';
import './NotifMenu'
import NotifMenu from './NotifMenu';
import LogoutButton from './LogOutButton'; 
import './LanguageDropdown'
import TextSizeControls from "./TextSizeControls";

import { useTranslation } from "react-i18next";
import { AuthContext } from '../context/AuthContext';
import { AccessibilityContext } from "../AccessibilityContext";

const Header = () => {
	const { t } = useTranslation();
	const { fontSize } = useContext(AccessibilityContext); 
	const { isLoggedIn } = useContext(AuthContext);

	return (
		<div>
			<nav className="navbar header mt-0 p-0" id="navbarID">
				<div className="container-fluid p-0">
					<nav className="d-flex flex-wrap menu" aria-label={t("Main Navigation")}>
						<Link style={{ fontSize: `${fontSize}px` }} aria-label={t("HeaderHome")} to="/" >{t("HeaderHome")}</Link>
						<Link style={{ fontSize: `${fontSize}px` }} aria-label={t("HeaderPlay")} to="/play">{t("HeaderPlay")}</Link>
						<Link style={{ fontSize: `${fontSize}px` }} aria-label={t("HeaderProfile")} to="/profile">{t("HeaderProfile")}</Link>
						<Link style={{ fontSize: `${fontSize}px` }} aria-label={t("HeaderAbout")} to="/about">{t("HeaderAbout")}</Link>
					</nav>
					<nav className="menu right-menu">
						<TextSizeControls/>
						<div className="notif" >
		{/*/<NotifMenu/>/*/}
						</div>
						{isLoggedIn ? (
                            <LogoutButton />
                        ) : (
                            <Link 	to="/login" 
									className="login" 
									style={{ fontSize: `${fontSize}px` }}
									aria-label={t("HeaderLogIn")}
							>
                                {t("HeaderLogIn")}
                            </Link>
                        )}
					</nav>
				</div>
			</nav>
		</div>
	);
};

export default Header;
