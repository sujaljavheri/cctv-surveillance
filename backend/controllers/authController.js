const User = require("../models/user");
const jwt = require("jsonwebtoken");

// ================= GENERATE TOKEN =================
const generateToken = (id) => {
  return jwt.sign({ id }, process.env.JWT_SECRET, { expiresIn: "30d" });
};

// ================= REGISTER USER =================
// @route  POST /api/auth/register
const registerUser = async (req, res) => {
  try {
    const { name, email, password } = req.body;

    // 🔴 Validation
    if (!name || !email || !password) {
      return res.status(400).json({ message: "Please fill all fields" });
    }

    // 🔴 Check existing user
    const userExists = await User.findOne({ email });
    if (userExists) {
      return res.status(400).json({ message: "User already exists" });
    }

    // ✅ Create user
    const user = await User.create({
      name,
      email,
      password,
    });

    // ✅ Response
    res.status(201).json({
      _id: user._id,
      name: user.name,
      email: user.email,
      token: generateToken(user._id),
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Server error" });
  }
};

// ================= LOGIN USER =================
// @route  POST /api/auth/login
const loginUser = async (req, res) => {
  try {
    const { email, password } = req.body;

    // 🔴 Validation
    if (!email || !password) {
      return res.status(400).json({ message: "Please enter email & password" });
    }

    // 🔍 Find user
    const user = await User.findOne({ email });

    // 🔐 Check password
    if (user && (await user.matchPassword(password))) {
      res.json({
        _id: user._id,
        name: user.name,
        email: user.email,
        token: generateToken(user._id),
      });
    } else {
      res.status(401).json({ message: "Invalid email or password" });
    }
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Server error" });
  }
};

// ================= GET PROFILE =================
// @route  GET /api/auth/profile (Protected)
const getUserProfile = async (req, res) => {
  try {
    if (!req.user) {
      return res.status(401).json({ message: "User not found" });
    }

    res.json({
      _id: req.user._id,
      name: req.user.name,
      email: req.user.email,
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Server error" });
  }
};

// ================= EXPORT =================
module.exports = {
  registerUser,
  loginUser,
  getUserProfile,
};
