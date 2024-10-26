// Importar dependencias necesarias
import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faShoppingCart, faStore, faUserCircle, faSignOutAlt, faSignInAlt, faUserPlus, faUtensils, faMapMarkerAlt } from '@fortawesome/free-solid-svg-icons';
import { Link } from 'react-router-dom';
import './Navbar.css'; // Archivo CSS que incluye los estilos del navbar

const Navbar = ({ user, cartCount }) => {
    return (
        <div className="new-navbar-wrapper">
            {/* Navbar Start */}
            <header id="new-navbar-header" className="new-navbar-static-header">
                <div className="new-navbar-main-header">
                    <div className="new-navbar-container">
                        <div className="new-navbar-row">
                            {/* Logo Section */}
                            <div className="new-navbar-logo">
                                <Link to="/" className="new-logo-link">
                                    <img src="/static/extra-images/logo-conexion.png" alt="CONEXIONGOURMET" className="new-navbar-logo-img" />
                                </Link>
                            </div>

                            {/* Search/Location Section */}
                            <div className="new-navbar-location">
                                <form action="#" className="new-navbar-location-form">
                                    <input type="text" name="location" placeholder="Enter your delivery location" autoComplete="off" className="new-navbar-location-input" />
                                    <button type="submit" className="new-navbar-location-btn">
                                        <FontAwesomeIcon icon={faMapMarkerAlt} />
                                    </button>
                                </form>
                            </div>

                            {/* Login & Marketplace Section */}
                            <div className="new-navbar-options">
                                {user?.isAuthenticated && (
                                    <Link to="/cart">
                                        <FontAwesomeIcon icon={faShoppingCart} className="text-danger" style={{ fontSize: '20px' }} />
                                        <span className="badge badge-warning" id="cart_counter" style={{ borderRadius: '50px', position: 'relative', bottom: '10px', left: '-5px' }}>
                                            {cartCount}
                                        </span>
                                    </Link>
                                )}

                                <Link to="/marketplace" className="new-navbar-marketplace">
                                    <FontAwesomeIcon icon={faStore} /> Marketplace
                                </Link>

                                {user?.isAuthenticated ? (
                                    <>
                                        <span className="new-navbar-user">Hola, {user.username}</span>
                                        <Link to="/myAccount" className="new-navbar-account">
                                            <FontAwesomeIcon icon={faUserCircle} /> My Account
                                        </Link>
                                        <Link to="/logout" className="new-navbar-logout">
                                            <FontAwesomeIcon icon={faSignOutAlt} /> Logout
                                        </Link>
                                    </>
                                ) : (
                                    <>
                                        <Link to="/login" className="new-navbar-login">
                                            <FontAwesomeIcon icon={faSignInAlt} /> Login
                                        </Link>
                                        <Link to="/registerUser" className="new-navbar-register">
                                            <FontAwesomeIcon icon={faUserPlus} /> Register
                                        </Link>
                                        <Link to="/registerVendor" className="new-navbar-register-restaurant">
                                            <FontAwesomeIcon icon={faUtensils} /> Register Restaurant
                                        </Link>
                                    </>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            </header>
        </div>
    );
};

export default Navbar;

