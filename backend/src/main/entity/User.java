package me.topeestla.hangmangame.entity;

import javax.persistence.*;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

/**
 * @author TopeEstLa
 */
@Entity
public class User implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;

    private String username;
    private int coins;

    @ElementCollection
    private List<String> purchased_avatars;
    @ElementCollection
    private List<String> purchased_gallows;

    private String avatar_equipped;
    private String gallows_equipped;

    public User() {
    }

    public User(int id, String username, int coins) {
        this.id = id;
        this.username = username;
        this.coins = coins;

        this.purchased_avatars = new ArrayList<>();
        this.purchased_gallows = new ArrayList<>();

        this.avatar_equipped = "default";
        this.gallows_equipped = "default";
    }

    public int getId() {
        return id;
    }

    public String getUsername() {
        return username;
    }

    public int getCoins() {
        return coins;
    }

    public void addCoins(int coins) {
        this.coins += coins;
    }

    public List<String> getPurchased_avatars() {
        return purchased_avatars;
    }

    public List<String> getPurchased_gallows() {
        return purchased_gallows;
    }

    public String getAvatar_equipped() {
        return avatar_equipped;
    }

    public String getGallows_equipped() {
        return gallows_equipped;
    }
}
