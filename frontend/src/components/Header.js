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
					<nav className="d-flex flex-wrap menu ">
						<Link style={{ fontSize: `${fontSize}px` }} to="/">{t("HeaderHome")}</Link>
						<Link style={{ fontSize: `${fontSize}px` }} to="/play">{t("HeaderPlay")}</Link>
						<Link style={{ fontSize: `${fontSize}px` }} to="/profile">{t("HeaderProfile")}</Link>
						<Link style={{ fontSize: `${fontSize}px` }} to="/about">{t("HeaderAbout")}</Link>
					</nav>
					<nav className="d-flex flex-wrap menu">
						<TextSizeControls/>
						{isLoggedIn ? (
                            <LogoutButton />
                        ) : (
                            <Link to="/login" className="login" style={{ fontSize: `${fontSize}px` }}>
                                {t("HeaderLogIn")}
                            </Link>
                        )}
					</nav>
			</nav>
		</div>
	);
};

export default Header;
