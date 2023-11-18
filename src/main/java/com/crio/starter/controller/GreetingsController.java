package com.crio.starter.controller;

import com.crio.starter.data.GreetingsEntity;
import com.crio.starter.exchange.ResponseDto;
import com.crio.starter.service.GreetingsService;
import lombok.RequiredArgsConstructor;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Sort;
import org.springframework.data.domain.PageRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor(onConstructor = @__(@Autowired))
public class GreetingsController {

  @Autowired
  private final GreetingsService greetingsService;

  @GetMapping("/memes")
  public List<GreetingsEntity> getMemes() {
    Sort sort = Sort.by(Sort.Direction.DESC, "id");
    PageRequest pageRequest = PageRequest.of(0, 100, sort);
    List<GreetingsEntity> memes = greetingsService.getMemes(pageRequest);
    if (memes.isEmpty()) {
      return Collections.emptyList();
    } else {
      return memes;
    }
  }


  @GetMapping("/memes/{id}")
  public ResponseEntity<GreetingsEntity> getMemeById(@PathVariable("id") String id) {
    Optional<GreetingsEntity> meme = greetingsService.getMemeById(id);
    if (meme.isPresent()) {
      return ResponseEntity.ok(meme.get());
    } else {
      return ResponseEntity.notFound().build();
    }
  }
 

  @PostMapping("/memes")
  public ResponseEntity<ResponseDto> createMeme(@RequestBody GreetingsEntity meme) {

    if (meme == null || meme.getName() == null || meme.getName().isEmpty() || meme.getUrl() == null
        || meme.getUrl().isEmpty() || meme.getCaption() == null || meme.getCaption().isEmpty()) {
      // Return a 400 Bad Request status if the meme data is empty
      return ResponseEntity.badRequest().build();
    }

    Optional<GreetingsEntity> existingMeme = greetingsService
        .getMemeByNameUrlAndCaption(meme.getName(), meme.getUrl(), meme.getCaption());

    if (existingMeme.isPresent()) {
      // Return a 409 if the meme already exists
      return ResponseEntity.status(HttpStatus.CONFLICT).build();
    } else {
      // Create a new meme if it doesn't already exist
      String new_meme_id = greetingsService.createMeme(meme);
      if (new_meme_id == "") {
        // return empty res;
        ResponseEntity.badRequest();
      }
      ResponseDto response = new ResponseDto(new_meme_id);
      return ResponseEntity.ok(response);
    }

  }


}