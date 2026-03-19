
functions { 
  compileinteger (word) {
      %funcall pushasinteger(word)
      @literalize
  }
}

subroutines {

 create {
      defsynonym blank ≡ 32
      %push (blank)
      @xword
      deftemp name ⇐ %pop
      %funcall create (name)
  }



}

invoke {
  @ok
}
