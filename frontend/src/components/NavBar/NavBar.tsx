import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import { useAuth } from "../../context";
import Modal from "../Modal/PopUpModal";
import { useState } from "react";

export default function NavBar() {
    const { user } = useAuth();
    const [showModal, setShowModal] = useState<boolean>(false);

    return (
        <Box sx={{ flexGrow: 1, bgcolor: "#E7DFC6" }}>
            <AppBar color="inherit" position="static">
                <Toolbar>
                    <IconButton
                        size="large"
                        edge="start"
                        color="inherit"
                        aria-label="menu"
                        sx={{ mr: 2 }}
                    >
                        <MenuIcon />
                    </IconButton>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                        Gestalt Notes
                    </Typography>
                    {user ? (
                        <Button color="inherit" onClick={() => console.log("Logging In")}>
                            Login
                        </Button>
                    ) : (
                        <Button
                            color="inherit"
                            onClick={() => setShowModal((prev) => !prev)}
                        >
                            Sign Up
                        </Button>
                    )}
                    {showModal && <Modal setShowModal={setShowModal}>Content</Modal>}
                </Toolbar>
            </AppBar>
        </Box>
    );
}
