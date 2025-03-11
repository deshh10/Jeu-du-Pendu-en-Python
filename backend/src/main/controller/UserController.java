package me.topeestla.hangmangame.controller;

import me.topeestla.hangmangame.entity.User;
import me.topeestla.hangmangame.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

/**
 * @author TopeEstLa
 */

@RestController
@RequestMapping("/user")
public class UserController {

    @Autowired
    private UserRepository userRepository;

    @GetMapping("/get/{username}")
    public ResponseEntity getUser(@PathVariable("username") String username) {
        Optional<User> user = userRepository.findByUsername(username);
        User user1 = null;

        if (user.isPresent()) {
            user1 = user.get();
        } else {
            user1 = new User(0, username, 0);
            userRepository.save(user1);
        }

        return new ResponseEntity(user1, HttpStatus.OK);
    }

    @PutMapping("/update/{username}")
    public ResponseEntity updateUser(@PathVariable("username") String username, @RequestBody String coins) {
        Optional<User> userFind = userRepository.findByUsername(username);
        User user = userFind.get();

        if (userFind.isPresent()) {
            user.addCoins(Integer.parseInt(coins));
            userRepository.save(user);
        }

        return new ResponseEntity(HttpStatus.BAD_REQUEST);
    }
}
