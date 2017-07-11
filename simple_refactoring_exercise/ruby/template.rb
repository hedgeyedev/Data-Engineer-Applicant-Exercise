module Template
  def template(source_template, req_id)
    ## define 'code' variable as string and pass to req_id
    code = String.new(req_id)
    ## concatination needed to match the %ALTCODE%
    altcode = code[0..4] + "-" + code[5..7]
    ## chained the sub method to subsitute the %CODE% and %ALTCODE%
    return source_template.sub(/%CODE%/, code).sub(/%ALTCODE%/, altcode)
  end
end
