import React, { useState } from "react";
import { NavLink as Link } from "react-router-dom";
import styled, { useTheme } from "styled-components";
import { DiCssdeck } from "react-icons/di";
import { FaBars } from "react-icons/fa";
// import meow from "../../images/sidd.jpg";

const Nav = styled.div`
  background-color: ${({ theme }) => theme.card_light};
  height: 80px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1rem;
  position: sticky;
  top: 0;
  z-index: 10;
  @media screen and (max-width: 960px) {
    transition: 0.8s all ease;
  }
`;

const Image = styled.img`
  position: relative;
  width: 10%;
  height: 10%;
  max-width: 400px;
  max-height: 400px;
  border-radius: 50%;
  border: 2px solid ${({ theme }) => theme.primary};

  @media (max-width: 768px) {
    max-width: 400px;
    max-height: 400px;
  }

  @media (max-width: 640px) {
    max-width: 280px;
    max-height: 280px;
  }
`;

const NavContainer = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  z-index: 1;
  width: 100%;
  padding: 0 24px;
  max-width: 1200px;
`;

const NavLogo = styled(Link)`
  display: flex;
  align-items: center;
  cursor: pointer;
  text-decoration: none;
`;

const MobileIcon = styled.div`
  display: none;
  @media screen and (max-width: 768px) {
    display: block;
    position: absolute;
    top: 50%;
    right: 24px;
    transform: translateY(-50%);
    cursor: pointer;
    color: ${({ theme }) => theme.text_primary};
  }
`;

const NavItems = styled.ul`
  display: flex;
  align-items: center;
  list-style: none;
  gap: 32px;
  margin: 0;
  
  @media screen and (max-width: 768px) {
    display: none;
  }
`;
const ButtonContainer = styled.div`
  display: flex;
  align-items: center;
  gap: 15px; /* Increased gap for better spacing */

  @media screen and (max-width: 640px) {
    display: none;
  }
`;

const Button = styled.a`
  background-color: transparent;
  // color: ${({ theme }) => theme.primary};
  color:red;
  // border: 1.8px solid ${({ theme }) => theme.primary};
  border: 1.8px solid red;
  border-radius: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 8px 20px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;
  white-space: nowrap; /* Prevents text wrapping */
  transition:200ms;
  
  &:hover {
    // background-color: ${({ theme }) => theme.primary};
    transform:scale(1.2);
    background-color:#641011;
    color: ${({ theme }) => theme.white};
  }

  @media screen and (max-width: 640px) {
    font-size: 0.8rem;
    padding: 8px 16px;
  }
`;

const Paddingg = styled.p`
display:inline;
width:100%;
padding:100px;
border: 10px solid red;
`

const StyledNavLink = styled.a`
  color: white;
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.2s ease-in-out;

  &:hover {
    color: ${({ theme }) => theme.primary};
  }
`;

export const Span = styled.div`
  padding: 0 4px;
  font-weight: bold;
  font-size: 18px;
`;


const MobileMenu = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  position: absolute;
  top: 80px;
  right: 0;
  width: 100%;
  padding: 12px 24px;
  background: ${({ theme }) => theme.card_light}99;
  transition: all 0.3s ease-in-out;
  transform: ${({ open }) => (open ? "translateX(0)" : "translateX(100%)")};
  opacity: ${({ open }) => (open ? "1" : "0")};
  z-index: ${({ open }) => (open ? "1" : "-1")};

  & > a, & > button {
    width: 100%; /* Ensures buttons take full width for better spacing */
    text-align: center;
    margin-bottom: 10px; /* Adds spacing between buttons */
  }
`;

const MobileMenuLinks = styled(StyledNavLink)`
  color: ${({ theme }) => theme.text_primary};
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.2s ease-in-out;

  &:hover {
    color: ${({ theme }) => theme.primary};
  }
`;

const Navbar = () => {
  const [open, setOpen] = useState(false);
  const theme = useTheme();

  return (
    <Nav>
      <NavContainer>

        <NavLogo to="/">
          {/* <DiCssdeck size="3rem" /> */}
          {/* <Image src={meow} alt="Hero" /> */}
          {/* <img src="../"></img> */}
          {/* <Image src={meow} alt="Hero" /> */}
          <Span>Tensor Titans</Span>
        </NavLogo>
        <MobileIcon onClick={() => setOpen(!open)}>
          <FaBars />
        </MobileIcon>
        <NavItems>
          <StyledNavLink href="#about">About</StyledNavLink>
          <StyledNavLink href="#projects">Models</StyledNavLink>
          <StyledNavLink href="https://1543siddhant.github.io/safetyhub-magnitude/" target="_blank">SafetyHub</StyledNavLink>
          <StyledNavLink href="https://1543siddhant.github.io/live-location-tracking-magnitude/" target="_blank">LocationTracking</StyledNavLink>
          <StyledNavLink href="https://1543siddhant.github.io/1543siddhant-incident-reporting-sys-magnitude/" target="_blank">ReportAnIncident</StyledNavLink>
          <StyledNavLink href="https://codebyte156.github.io/search-report/searchreport.html" target="_blank">Search</StyledNavLink>
          {/* <StyledNavLink href="https://example.com" target="_blank"></StyledNavLink> */}
        </NavItems>
        <ButtonContainer>
          <Button href="http://127.0.0.1:5007" target="_blank" rel="noopener noreferrer">
            Emergency SOS
          </Button>
        </ButtonContainer>
      </NavContainer>
      {open && (
        <MobileMenu open={open}>
          <MobileMenuLinks href="#about" onClick={() => setOpen(!open)}>
            About``
          </MobileMenuLinks>
          <MobileMenuLinks href="#skills" onClick={() => setOpen(!open)}>
            Skills
          </MobileMenuLinks>
          <MobileMenuLinks href="#experience" onClick={() => setOpen(!open)}>
            Experience
          </MobileMenuLinks>
          <MobileMenuLinks href="#projects" onClick={() => setOpen(!open)}>
            Projects
          </MobileMenuLinks>
          <MobileMenuLinks href="#education" onClick={() => setOpen(!open)}>
            Education
          </MobileMenuLinks>
          
          <Button
            href="https://github.com/1543siddhant"
            target="_blank"
            rel="noopener noreferrer"
            style={{ background: theme.primary, color: "white" }}
          >
            Github
          </Button>
          <Button
            href="https://www.linkedin.com/in/siddhant-patil-04587525b/"
            target="_blank"
            rel="noopener noreferrer"
            style={{ background: theme.primary, color: "white" }}
          >
            LinkedIn
          </Button>
          <Button
            href="https://drive.google.com/file/d/1yHSKg7waygaev_fgneCotIVIrh3Y5H0b/view"
            target="_blank"
            rel="noopener noreferrer"
            style={{ background: theme.primary, color: "white" }}
          >
            Resume
          </Button>
        </MobileMenu>
      )}
    </Nav>
  );
};

export default Navbar;